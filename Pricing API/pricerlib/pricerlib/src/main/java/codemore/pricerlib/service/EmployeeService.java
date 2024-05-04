package codemore.pricerlib.service;

import codemore.pricerlib.exception.UserNotFoundException;
import codemore.pricerlib.model.Employee;
import codemore.pricerlib.pricing.model.equity.BlackScholesEquity;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;
import codemore.pricerlib.repository.EmployeeRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.UUID;

@Service
public class EmployeeService {
    private final EmployeeRepo employeeRepo;

    // To be used in pricing function
    private EuropeanCall call = new EuropeanCall();
    private BlackScholesEquity bsModel = new BlackScholesEquity();

    @Autowired
    public EmployeeService(EmployeeRepo employeeRepo){
        this.employeeRepo = employeeRepo;
    }

    // Add employee to employeeRepo
    public Employee addEmployee(Employee employee){
        employee.setEmployeeCode(UUID.randomUUID().toString());
        return employeeRepo.save(employee);
    }

    public List<Employee> findAllEmployees(){
        return employeeRepo.findAll();
    }

    public Employee updateEmployee(Employee employee){
        return employeeRepo.save(employee);
    }

    public void deleteEmployee(Long id){
        employeeRepo.deleteEmployeeById(id);
    }

    public Employee findEmployeeById(Long id){
        return employeeRepo.findEmployeeById(id).orElseThrow(() -> new UserNotFoundException("User by id" + id + " was not found."));
    }


    /********************************************
     PRICING FUNCTIONS
     ********************************************/
    public Double getBSPrice(Double sigma){
        // Create new parameter HashMap
        HashMap<String, Double> newParameter = new HashMap<>();
        newParameter.put("sigma", sigma);

        // Set the vol parameter
        bsModel.setParameters(newParameter);
        Double price = call.price(bsModel);
        return price;
    }
}
