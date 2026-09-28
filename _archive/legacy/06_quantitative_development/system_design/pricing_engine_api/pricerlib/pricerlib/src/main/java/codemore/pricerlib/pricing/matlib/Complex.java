package codemore.pricerlib.pricing.matlib;

import static java.lang.Math.*;

public class Complex {
    private double real, complex;

    public Complex(){
        real = 0.0;
        complex = 0.0;
    }

    public Complex(double real){
        this.real = real;
        this.complex = 0.0;
    }

    public Complex(double real, double complex){
        this.real = real;
        this.complex = complex;
    }

    public void print(){
        System.out.println("(" + real + "+" + complex + "i)");
    }

    public double real(){
        return this.real;
    }

    public double complex(){
        return this.complex;
    }

    public Complex add(double real){
        this.real += real;
        return this;
    }

    public Complex add(Complex z){
        this.real += z.real;
        this.complex += z.complex;
        return this;
    }

    public Complex subtract(double real){
        this.real -= real;
        return this;
    }

    public Complex subtract(Complex z){
        this.real -= z.real;
        this.complex -= z.complex;
        return this;
    }

    public Complex multiply(double real){
        this.real *= real;
        this.complex *= real;
        return this;
    }

    public Complex multiply(Complex z){
        /*********************************
          Multiply complex numbers:
          (x1+y1i)*(x2+y2i) = (x1*x2 - y1*y2) + (x1*y2 + y1*x2)

        * ********************************/
        this.real = this.real * z.real - this.complex * z.complex;
        this.complex = this.real * z.complex + this.complex * z.real;
        return this;

    }

    public Complex divide(double real){
        this.real /= real;
        this.complex /= real;
        return this;
    }

    public Complex divide(Complex z){
        double zReal = z.real;
        double zComplex = z.complex;
        double denom = zReal*zReal + zComplex*zComplex;

        double newReal = (this.real*zReal + this.complex*zComplex)/denom;
        double newComplex = (zReal*this.complex - this.real*zComplex)/denom;

        this.real = newReal;
        this.complex = newComplex;

        return this;
    }

    public static Complex log(Complex z){
        /*********************************
         Log of complex numbers:

         For complex number z, the log of the complex number z is:
         log z = log (x + yi)
               = ln(x*x + y*y) + i * atan2(y, x)
         * ********************************/
        double r = sqrt(z.real*z.real + z.complex * z.complex);
        double x = z.real;
        double y = z.complex;

        z.real = Math.log(r);
        z.complex = atan2(y, x);

        return z;
    }

    public static Complex exp(Complex z){
        double x = z.real;
        double y = z.complex;

        z.real = Math.exp(x) * Math.cos(y);
        z.complex = Math.exp(x) * Math.sin(y);

        return z;
    }

    public static Complex pow(Complex z,  double c){
        Complex logZ = Complex.log(z).multiply(c);
        return Complex.exp(logZ);

    }

}
