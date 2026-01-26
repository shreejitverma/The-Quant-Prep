package codemore.pricerlib.exception;

public class UserNotFoundException extends RuntimeException{
    public UserNotFoundException(String message) {
        // Pass message from super class
        super(message);
    }
}
