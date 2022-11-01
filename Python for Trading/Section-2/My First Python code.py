
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Let us begin
# 
# Now that you have learned how to setup Anaconda, it is time to understand how to code programs in Python. Python uses a simple syntax which makes it very easy for someone learning to program for the first time. This notebook is comprehensively designed to help you get familiarized with programming and learn basics of Python.

# ## What is programming?
# 
# Programming is the way of telling a machine what to do. This machine might be your computer, smartphone, or tablet. The task might be something as simple as noting down today’s date or capturing information about the Earth’s atmosphere on a satellite. Programming has a lot of alias names and they’re used interchangeably. It goes by programming, developing, or coding all of which involves creating software that gets a machine to do what you want it to do.

# ### Hello World Program
# 
# How would you make Python print "Hello World" for you? Well, it's never been this easy, just use the <b> print </b> command.

# In[1]:


print ("Hello World!")


# In[2]:


# You may try other variations
print ("I am new to programming!")
print ("Python is cool!")


# ## Introduction to Python programming
# Python design places more weight on coding productivity and code readability. Python
# makes use of simple syntax which looks like written English. It talks with words and
# sentences, rather than characters. Python is a portable language. Python can be installed
# and run on any computer.
# 
# Python coding is a lot fun and is easy. Take this python code for an example:
# 

# In[3]:


x = 2
y = 3
sum = x + y
print (sum)


# Even without any coding background, you can easily make out that the code adds up two numbers and prints it. You may modify the code above and try different mathematical operations on different variables.

# ## Variables, Data Types and Objects
# 
# We have studied how to use a variable in python in the previous video unit.

# In[ ]:


x = 100


# One thing to keep in mind, the equal '=' sign used while assigning a value to a variable. It should not be read as 'equal to'. It should be read or interpreted as "is set to". 
# 
# In the previous example, we will read that the value of variable 'x' <b>is set to</b> '100'.

# In[ ]:


y = 50 # Initialising a new variable 'y' whose value is set to 50


# ### ID of an object
# The keyword <b>id ()</b> specifies the object's address in memory. Look at the code below for seeing the addresses of different objects.

# In[ ]:


id (x)


# You may change the variable name inside the function id() to print the id's of other variables.

# In[ ]:


id (y)


# Note : The IDs of 'x' and 'y' are different.

# ### Data Type of an Object
# 
# The type of an object cannot change. It specifies two things, the operations that are allowed and the set of values that the object can hold. The keyword type() is used to check the type of an object.

# In[ ]:


type (x)


# In[ ]:


type (y)


# Now, let us try something more.

# In[ ]:


x = x + 1.11
print (x)      # This will print the new value of 'x' variable
type(x)        # This will print the most updated data type of 'x'


# Now you may check the ID of the new 'x' object which is now a float and not a integer.

# In[ ]:


id (x)


# Note this is different form the 'int x' ID. 
# 
# Python automatically takes care of the physical representation of different data types i.e. an integer value will be stored in a different memory location than a float or string.

# In[ ]:


# let us now convert variable 'x' to a string data type and observe the changes

x = "hundred"
print (x)
type (x)


# In[ ]:


id (x)


# ### Object References
# 
# Let us observe the following code.

# In[ ]:


a = 123
b = a


# Where will the object point? Will it be to the same object ID?

# In[ ]:


id (a)


# In[ ]:


id (b)


# Yes, Since same value is stored in both the variables 'a' and 'b', they will point to the same memory location or in other words, they will have the <b>same object ID</b>.

# ## Multi-Line Statements
# 
# There is no semicolon to indicate an end of statement and therefore Python interprets the end of line as the end of statement.
# 
# For example, a code to calculate total marks.

# In[ ]:


biology_marks = 82
physics_marks = 91
maths_marks = 96
chemistry_marks = 88
total_marks = biology_marks + physics_marks + maths_marks + chemistry_marks
print (total_marks)


# However, if a line is too long, code can be made readable by adding a split, to a single line of code and convert them into multiple lines. In such scenarios, use  backward slash as line continuation character to specify that the line should continue.
# 

# In[ ]:


total_marks = biology_marks +               physics_marks +               maths_marks +               chemistry_marks
print (total_marks)


# ##  Indentation
# 
# Python forces you to follow proper indentation. The number of spaces in indentation can be different, but all lines of code within the same block should have the same number of spaces in the indentation.
# 
# For example, the 3rd line of the code in the cell below shows incorrect indentation. Try running the code to see the error that it throws.

# In[ ]:


# Python Program to calculate the square of number
num = 8
   num_sq = num ** 2
print (num_sq)


# In[ ]:


# On removing the indent
num = 8
num_sq = num ** 2
print (num_sq)


# ## Further Resources
# 
# As you begin your journey of learning Python programming, we would recommend you to extensively use freely available resources online to understand simple syntax and application of available Python libraries. You can use these following resources in addition to others available online:
# 1. http://docs.python.org/reference/introduction.html
# Reference manual
# 2. http://wiki.python.org/moin/BeginnersGuide
# A guide for writing and running Python programs
