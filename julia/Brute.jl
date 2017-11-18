#!/usr/bin/julia

module Brute

ITER = 250
MEM = 15

#G = 6.67408e-11
G = 1

DIM = 3
N = 100
DT = 0.001

type System
    pos::Array{Float64,2}
    vel::Array{Float64,2}
    mass::Array{Float64,1}
end

function init()
    theta = 2*pi*rand(N)
    r = 0.5 + randn(N)
    x = r .* cos.(theta)
    y = r .* sin.(theta)
    z = randn(N) / 3

    pos = hcat(x,y,z)'
    vel = 4*rand(DIM, N)-2
    return System(pos, vel, ones(N))
end

function col_norms(matrix)
    norms = zeros(Float64, size(matrix, 2))
    for col in 1:size(matrix, 2)
        for row in 1:size(matrix, 1)
            norms[col] += matrix[row, col]^2
        end
        norms[col] = sqrt(norms[col])
    end
    return norms
end


function update!(sys::System)
    for i = 1:N
        others = cat(1, 1:i-1, i+1:N)
        pos_others = view(sys.pos, :, others)

        dist = repmat(sys.pos[:,i], 1, N-1) - pos_others
        denom = col_norms(dist).^(3/2)

        for dim = 1:3
            sys.vel[dim,i] -= DT * G * sum(sys.mass[others] .*
                                           dist[dim,:] ./ denom)
        end
    end
    sys.pos += DT * sys.vel
    return
end


function old_update!(sys::System)

    for i = 1:N-1
        for j = i+1:N
            # Force between this pair
            r = sys.pos[:,i] - sys.pos[:,j]
            f_ij = - G * sys.mass[i] * sys.mass[j] * r / norm(r)^(3/2)
            # Update this pair accordingly
            sys.vel[:,i] += DT * f_ij / sys.mass[i]
            sys.vel[:,j] -= DT * f_ij / sys.mass[j]
        end
    end
    sys.pos += DT * sys.vel
    map(i-> push!(sys.hist[i], sys.pos[:,i]), 1:N)
    if size(sys.hist[1], 1) > MEM
        map(i-> shift!(sys.hist[i]), 1:N)
    end
    return
end


function main()
    sys = init()
    map(m-> print(m," "),sys.mass)
    print("\n")
    i = 0
    while true
        i += 1

        update!(sys)
        update!(sys)
        update!(sys)

        print(1, "\n")
        map(x-> print(x," "),sys.pos[1,:])
        print("\n")
        map(y-> print(y," "),sys.pos[2,:])
        print("\n")
        map(z-> print(z," "),sys.pos[3,:])
        print("\n")

        if i % 10 == 0
            write(STDERR, string(i))
            write(STDERR, "\n")
        end
    end
end

end

Brute.main()
