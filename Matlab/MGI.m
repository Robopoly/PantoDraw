function [ q1, q2 ] = MGI( x,y,L1,L2,a )


for i = 1:size(x,1)
    for j = 1:size(x,2)
        E = [x(i,j);y(i,j)];
        
        M1 = [-a/2;0];
        M2 = [a/2;0];
        E1p = E-M1;
        E2p = E-M2;
        
        q1(i,j) = acos((norm(E1p)^2 + L1^2 - L2^2)/(2*norm(E1p) * L1)) + atan2(E1p(2), E1p(1));
        q2(i,j) = acos((norm(E2p)^2 + L1^2 - L2^2)/(2*norm(E2p) * L1)) + pi - atan2(E2p(2), E2p(1));
    end
end
end

