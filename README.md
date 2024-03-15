%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Figura resistencias
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rango=[-20 60]

tempC=rango(1) :0.01:rango(2);
B=4500
R=100000


Rt= @(t,b)(R * exp(b*((1./(273+t))-(1/298))))
Rp= @(t,b)(Rt(t,b) .* ((b-(2.*(273+t)))./(b+(2.*(273+t))))) 
f=@(t,b) (-b^3 ./ (t.^2 .*(b^2 - 4*(t.^2) )).*Rp(t,b))

Req=@(t,b) ((Rt(t,4500).*Rp(20,4500))./(Rt(t,4500)+Rp(20,4500)) )

plot(tempC,Req(tempC,B))
hold on
plot(tempC,Rt(tempC,B))
hold on
plot(tempC,1e5*ones(length(tempC)))
ylim([0 2e5])
legend('Req','Rt(T)','Ro')
hold off