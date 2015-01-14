function [x, y] = MGD(q1,q2, L1, L2, a)

A1 = [L1*cos(q1)-a/2; L1*sin(q1)];
A2 = [-L1*cos(q2)+a/2; L1*sin(q2)];

A1A2 = A2-A1;
A1A2p = [-A1A2(2);A1A2(1)];

E = A1 + A1A2./2 + A1A2p./norm(A1A2p) .* sqrt(L2.^2 - (norm(A1A2)/2).^2);
x = E(1);
y = E(2);

end