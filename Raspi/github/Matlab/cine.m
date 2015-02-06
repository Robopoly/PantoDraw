
%%

close all;
%Variables
syms q1 q2 L2 a;
L1 = 1;

%Working area
betaMax = 30 * pi/180;
yb = sqrt(L1^2 + L2^2 - 2*L1*L2*cos(betaMax));
ratio = 1.5;
syms alpha;
h = (L1+L2)*sin(alpha) - yb;
w = 2*(L1 + L2)*cos(alpha) - a;
area = h*w;
alphaV = solve(ratio*h==w,alpha,'Real',true);
alpha = alphaV(2);
area = subs(area);
h = subs(h);
figure
ezsurf(area,[0,4,0,2]);
title('Working area depending on L2 and a')
%MGD computation
[Ex,Ey] = MGD(q1,q2,L1,L2,a);
E = [Ex;Ey];

%Jacobian
q = [q1; q2];
J = jacobian(E,q);
Jx1 = J(1,1);
Jx2 = J(1,2);
Jy1 = J(2,1);
Jy2 = J(2,2);

%Middle working point (q1 = q2, higher force transmission)
qm = atan(L2/L1) + acos(a/2 / sqrt(L2^2 + L1^2));
%Other middle point. Working area center
%qm = MGI(0,yb + h/2,L1,L2,a);
%Spacial derivative at point qm
dym = subs(J,{q1,q2},{qm,qm}) * [-1;-1];
dym = dym(2);
dxm = subs(J,{q1,q2},{qm,qm}) * [-1;1];
dxm = dxm(1);

%parameters a and L2 to have an equal resolution on x and y
figure
ezsurf(dxm,[0,4,0,2]);
hold on;
ezsurf(dym,[0,4,0,2]);
title('Dx and Dy depending on L2 and a, at nominal point')
figure;
ezplot(dxm == dym,[0,4,0,2])
title('Dx == Dy, at nominal point');
%One find that a ~= (L2-1) * 2/1.4
a = (L2-L1) * 2/1.4;

figure
ezplot(subs(area),[0,4]);
title('Working area depending on L2')

%Plot dym function of L2
figure;

ezsurf(subs(subs(dxm,qm,q1)),[1,10,0,2*pi])
title('Dx depending on L2 and q1==q2, on vertical axis')
figure
ezsurf(subs(subs(dym,qm,q1)),[1,10,0,2*pi])
title('Dy depending on L2 and q1==q2, on vertical axis')

%One find that L2 doesn't change sensibility for q1 = q2 for L2 = 1*L1.
%What about the rest?

%Find values for Ey = Eym, and Ex = Ex
Ex = subs(Ex);
Ey = subs(Ey);
Eym = subs(subs(Ey,{q1,q2},{qm,qm}));

x = -L1/2:0.5:L1/2;
y = (-L1/2 + Eym):0.5:(L1/2+Eym);

% [X,Y] = meshgrid(x,y);
% [q1v,q2v] = MGI(X,Y,L1,L2,a);
% 
% q1v = subs(q1v);
% q2v = subs(q2v);
% 
% Jx1m = subs(Jx1,{q1,q2},{q1v,q2v});
% Jx1m = subs(Jx1m);
% Jx2m = subs(Jx2,{q1,q2},{q1v,q2v});
% Jx2m = subs(Jx2m);
% Jy1m = subs(Jy1,{q1,q2},{q1v,q2v});
% Jy1m = subs(Jy1m);
% Jy2m = subs(Jy2,{q1,q2},{q1v,q2v});
% Jy2m = subs(Jy2m);
% 
% Jm = sqrt((abs(Jx1m) + abs(Jx2m)).^2 + (abs(Jy1m) + abs(Jy2m)).^2);
% figure;
% L2v = 1:0.5:4;
% 
% 
% for i = 1:size(Jx1m,1)
%     for j = 1:size(Jx1m,2)
%         
%         Jmt = double(subs(Jm(i,j),L2v));
%         plot(L2v,Jmt);
%         hold on;
%         drawnow;
%     end
% end


%%
%Final plots
close all
%Variables
syms q1 q2
L1 = 90;
L2 = 90*1.4;
a = (L2-1*L1) * 2/1.4;
betaMax = 30 * pi/180;
yb = sqrt(L1^2 + L2^2 - 2*L1*L2*cos(betaMax));
ratio = 1.5;
syms alpha;
h = (L1+L2)*sin(alpha) - yb;
w = 2*(L1 + L2)*cos(alpha) - a;
area = h*w;
alphaV = solve(ratio*h==w,alpha,'Real',true);
alpha = max(double(alphaV));
area = double(subs(area));
h = double(subs(h));
w = double(subs(w));

%Working area
H = 100;
W = 150;

%MGD computation
[Ex,Ey] = MGD(q1,q2,L1,L2,a);
E = [Ex;Ey];

%Jacobian
q = [q1; q2];
J = jacobian(E,q);
Jx1 = J(1,1);
Jx2 = J(1,2);
Jy1 = J(2,1);
Jy2 = J(2,2);
Jm = sqrt((abs(Jx1) + abs(Jx2))^2 + (abs(Jy1) + abs(Jy2))^2);
%Middle working point (q1 = q2, higher force transmission)
qm = atan(L2/L1) + acos(a/2 / sqrt(L2^2 + L1^2));
[qm,qm] = MGI(0,yb + h/2,L1,L2,a);

%Spacial derivative at point qm
dym = J * [-1;-1];
dym = dym(2);
dxm = J * [-1;1];
dxm = dxm(1);

figure
ezsurf(dym,[0,pi])
figure
ezsurf(dxm,[0,pi])
figure
ezplot(subs(dym,q1,q2), [0,2*pi]);
hold on
ezplot(subs(dxm,q1,q2), [0,2*pi]);
axis tight
figure
ezplot(subs(Ey,q1,q2), [0,2*pi]);


Eym = subs(subs(Ey,{q1,q2},{qm,qm}));
Eym = double(Eym);

x = -W/2:W/2:W/2;
y = (-H/2 + Eym):H/2:(H/2+Eym);

[X,Y] = meshgrid(x,y);
[q1v,q2v] = MGI(X,Y,L1,L2,a);

Jmarea = double(subs(Jm,{q1,q2}, {q1v, q2v}));

qmax = max(q1v(:))
qmin = min(q1v(:))

Jmax = max(Jmarea(:))
Jmin = min(Jmarea(:))
Jmean = mean(Jmarea(:))



A1 = [L1*cos(q1)-a/2; L1*sin(q1)];
A2 = [-L1*cos(q2)+a/2; L1*sin(q2)];
A1E = E-A1;
A2E = E-A2;
A1A2 = A2-A1;

%Constrains
[q1,q2] = meshgrid(qmin:0.1:qmax,qmin:0.1:qmax);
% cons = (double(subs(atan2(A1E(2),A1E(1)))) < q1) & ((cos(q1)+cos(q2))*L1 < a) & (double(subs(atan2(A2E(2),-A2E(1)))) < q2) & (double(subs(norm(A1A2))) < 2*L2);
% cons = double(cons);
% 
% qAdm = cons .* q1;




Exp = subs(Ex);
Eyp = subs(Ey); 

figure
plot(Exp(:), Eyp(:),'*');
Lx = [W/2, W/2, -W/2, -W/2, W/2];
Ly = [H/2+Eym, -H/2+Eym, -H/2+Eym, H/2+Eym, H/2+Eym];
line(Lx,Ly)
line([L1+L1, -L1-L2],[yb,yb])
axis equal;
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 