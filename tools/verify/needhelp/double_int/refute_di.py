from sympy import *
x,y,u=symbols('x y u')
print(integrate(integrate(1,(y,0,x)),(x,0,2)), integrate(x*y,(y,0,3),(x,0,2)))
print(integrate(integrate(1,(y,x**2,x)),(x,0,1)), integrate(integrate(x,(x,y,sqrt(y))),(y,0,1)))
print(integrate(x*(4-x**2),(x,0,2)), integrate(sqrt(y),(y,0,4)))
print(N(integrate(2*x*exp(x**2),(x,0,1))), integrate(sin(y),(y,0,pi)), N(integrate(y*sin(y**2),(y,0,1))))
print(integrate(2-2*y,(y,0,1)), integrate(y*(2-2*y),(y,0,1)), pi/2, 3*pi/4, N(Rational(3,2)*log(2)))
