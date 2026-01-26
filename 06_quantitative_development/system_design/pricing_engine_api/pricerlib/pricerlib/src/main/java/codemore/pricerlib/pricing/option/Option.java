package codemore.pricerlib.pricing.option;
import codemore.pricerlib.pricing.model.*;

public interface Option{
    /***************************************************
     Generic interface to represent every single option to be priced

     Only a single function is needed, the pricer function.
     ****************************************************/
    double price(Model model);

}
