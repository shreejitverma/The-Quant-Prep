package codemore.pricerlib.pricing.option.pathindependent;

import codemore.pricerlib.pricing.model.Model;

public interface PathIndependentOption<T extends Model> {
    /***************************************************
     Generic interface to represent every path independent option to be priced. Mostly European options.

     Only a single function is needed, the pricer function.
     ****************************************************/
    public double price(T model);
}
