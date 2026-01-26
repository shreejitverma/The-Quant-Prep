
# coding: utf-8

# ## Notebook Instructions
# 
# <i> You can run the notebook document sequentially (one cell a time) by pressing <b> shift + enter </b>. While a cell is running, In [*] will display on the left. When it has been run, a number will display indicating the order in which it was run in the notebook. Example: In [8]: </i>
# 
# <i> Enter edit mode by pressing <b> Enter </b> or using the mouse to click on a cell's editor area. Edit mode is indicated by a green cell border and a prompt showing in the editor area. </i>

# ## Lists as Stacks
# 
# A stack is a collection of objects which work as per the <b>LIFO - Last in First Out</b> principle. Consider a simple example: You are throwing a dinner party at your place. You will place a stack of plates at the buffet table. Whenever you are adding new plates to the stack, you will place the plates at the top. Similarly, whenever a guest takes a plate, he/she will take it from the top of the stack. This is the Last in, First Out principle.
# 
# In the world of programming it, learning LIFO for data is very handy. We will do the same in the upcoming code. When you add items to the stack, it is known as <b>push operation</b>. You will do this using the append ( ) method.  When you remove items from a stack, it is known as <b>pop operation</b>. You actually have a pop ( ) method in python.
# 
# This is not something new which you have learnt. But understanding how data works in a stack (LIFO principle) is important, since this concept is used for evaluating expressions and syntax parsing, scheduling algorithms, routines, writing effective functions and so on.

# In[54]:


# Bottom --> 10, 20, 30, 40, 50 --> Top

my_stack = [10, 20, 30, 40, 50] # List

my_stack.append (60) # The PUSH OPERATION

print (my_stack) 


# In[55]:


# New Stack: Bottom ---> 10, 20, 30, 40, 50, 60 ---> Top

my_stack.pop () # The POP OPERATION

my_stack.pop () # The same operation 'twice' 

print (my_stack) # From the 'top', 50 and 60 will be removed.


# ## Lists as Queues
# 
# A <b>queue</b> is a collection of objects which works as per the FIFO - First in First Out principle. Consider a simple example: You are at the concert to listen to your favourite artist. The tickets for this concert are in great demand. Hence, all the fans form a queue outside the ticket collection centre. The fan to arrive first, will be the first one to get the ticket while the one to arrive last may or may not get the ticket. This is the <b>First in, First Out</b> principle.

# In[56]:


# 'collections' is a package which contains high performance container datatyes

# 'deque' us a list-like container with fast appends and pops on either ends

from collections import deque

# This is your queue. "Roger Federer" is the first to arrive while "Novak Djokovic is the last.

my_queue = deque(["Roger Federer", "Rafael Nadal", "Novak Djokovic"])

my_queue.append ("Andre Agassi") # Now Andre Agassi arrives 

my_queue.append ("Pete Sampras") # Now Pete Sampras arrives

print (my_queue) # You may have a look at the queue below


# In[57]:


my_queue.popleft() # The first to arrives leaves first


# In[58]:


my_queue.popleft() # The second to arrive leaves now


# In[59]:


print (my_queue) # This is your present queue in the order of arrival


# Using <b>deque</b> from the <b>collection</b> module is one way of doing it.
# 
# Another way of doing this is using the <b>insert()</b> and <b>remove()</b> functions. However, lists as queues are not that efficient. Adding and removing from the beginning of the list is slow since all the elements have to be shifted by one.

# ## Graphs
# 
# (Optional Read)
# 
# A graph in computer science is a network consisting of different <b>nodes</b> or <b>vertices</b>. These nodes may or may not be connected to each other. The line that joins the nodes is called an <b>edge</b>. If the edge has a particular direction it is a <b>directed graph</b>. If not, it is an <b>undirected graph</b>.

# This is an example of an Undirected Graph, where A, B, C, D and E are the various nodes. The following list shows that these five nodes are connected to which other nodes. For diagram, you may refer to the graph, taught in the video lecture.
# 
# A <---> B,C <br>
# B <---> A,C,D <br>
# C <---> A,B,D,E <br>
# D <---> B,C,E <br>
# E <---> D,C <br>

# In[61]:


# Please Note: At present we are using dictionaries, functions and loops which have not been taught.

# We will take up all of these concepts in the upcoming units or sections of this course.


# The following code is just to display all the different edges of the graph, as shown in the video lecture.

my_graph = {'A' : ['B', 'C'], 'B': ['A','C','D'], 'C' : ['A','B','D','E'], 'D': ['B','C','E'], 'E': ['D','C']}


# In[62]:


def define_edges(my_graph):
    edges = []
    for nodes in my_graph:
        for adjacent_nodes in my_graph [nodes]:
            edges.append((nodes, adjacent_nodes))
    return edges

print(define_edges(my_graph))


# ## Trees
# 
# (Optional Read)
# 
# A 'tree' in real world has roots below the ground, a trunk, and the branches that are spread all across the trunk in an organised way. These branches have leaves on them.
# 
# In the programming world, a tree is upside down of what you see in the real world. At the top is the <b>root node</b>. The other node that follow the root node are called <b>branch nodes</b>. The final nodes of these branches are called <b>leaf nodes</b>.

# In[63]:


# In the code below, we have shown how to 'travel' through a tree. The tree is same as that shown in the video lecture.

# We have done this wih the help of 'classes'. We have no covered classes.


# In[64]:


class Tree:
    def __init__(self, info, left=None, right=None):
        self.info = info
        self.left  = left
        self.right = right

    def __str__(self):
        return (str(self.info) + ', Left node: ' + str(self.left) + ', Right node: ' + str(self.right))

tree = Tree("Root Node", Tree("Branch_1", "Leave_1", "Leave_2"), Tree("Branch_2", "Leave_3", "Leave_4"))
print(tree)


# ### In the upcoming iPython Notebook
# 
# We will see a new data structure called <b>'Dictionary'</b>. 
# 
# #### So, Stay Tuned!
