<h1 align="center">Quick Covering Tool</h1>

<br>

|             | Authors         | Contact                        |
|-------------|-----------------|-------------------------|
| Author:     | M.Sina Ertugrul | m.s.ertugrul@gmail.com  |
| Supervisor: | Naoki Kanazawa  | nkanazawa1989@gmail.com |

<br>

<p align="center">
<img width="250px" height="250px" src="https://github.com/Musa-Sina-Ertugrul/Qiskit_OOAD_Proposal_RFC0014/assets/102359522/90669ecd-eaca-4724-b97c-d98a7fb67aa6">
</p>

<h5>About Me ( M.Sina Ertugrul ) </h5>

> NOTE: I am an undergrad and I do not know the Qiskit framework and quantum programming as expected from an undergrad but, I have worked with
scientists during my internships ( One of Turkey's best bioinformatics research center ) and I know how scientists code, what their code looks like,
how scientific codes can be repetitive or require small tasks

<h3 align="center">Introduction</h3>
<h1 align="center"></h1>

Scientific researches sometimes require small or repetitive tasks and writing code for those tasks can be repetitive and tedious. People do not want repetitive code as you know. 
Therefore, we need a solution for repetitive code chunks and the main reason for repetitive code chunks is the template method pattern ( This topic held on Qiskit Experiment OSS 
Public Team Presentation ). But this pattern is essential for current implementation and for creating new or creative experiments, so we decided to go around this pattern.
Our implementation mimics <b><i>Decimal</i></b> class in Python STL. Decimal class can change its functionality with <b><i>with</i></b> keyword and in our suggestion main object that runs the experiment's
functionalities will be changed by <b><i>BaseManager</i></b> class and after turning past indentation they will be vanished

<h3 align="center">BaseManager Class</h3>
<h1 align="center"></h1>

```python

class BaseManager:
    
    def __init__(self, target : BaseAnalysis | BaseExperiment,
                 current : BaseAnalysis | BaseExperiment) -> None:
        self.__target = target
        self.__current = current
        self.__old_instance_methods : dict = dict()
    
        class DeafultAttr:
            
            pass
        
        self.__base_attr = DeafultAttr.__dict__
    
    def __enter__(self):
        return self
    
    def __call__(self):
        
        self.__old_instance_methods = {key : value for key,value in 
                                       self.__target.__class__.__dict__.items() 
                                       if (current_atr := self.__current.__class__. \
                                       __dict__.get(key,False)) and current_atr not in
                                       self.__base_attr and 
                                       isinstance(current_atr,FunctionType)}
        
        for obj_method_key in self.__old_instance_methods.keys():
            
            setattr(self.__target,obj_method_key,
                    MethodType(self.__current.__class__.__dict__[obj_method_key],
                               self.__target))
        return self.__target
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        for obj_method_key in self.__old_instance_methods.keys():
            
            delattr(self.__target,obj_method_key)

```

As you can see <b><i>BaseManager Class</i></b> follow this instructions:

* Storing old method names.
* Bounding new methods with object
* Deleting new methods

> As you know Python works with namespaces and Python interpreter searches keys with top to bottom approach
so, we do not need to change the values of old methods. We need to add same key and new method value pair to the upper namespace

<h3 align="center">Usage</h3>
<h1 align="center"></h1>

You can check ./example.ipynb for pseudo-usage

<h3 align="center">Things to Do</h3>
<h1 align="center"></h1>

* Designing <b><i>BaseManager Class</i></b> for our good

* Implementing code and tests

* The Qiskit Experiment OSS Public Team has pretty valuable physicists and they use the Qiskit framework during daily tasks so they can identify
small experiments or repetitive code chunks and can turn them into predefined classes so, our <b><i>BaseManager Class</i></b> can manage code chunks with ease

* Preparing documentation for the new feature

* Identifying new usage or implementation patterns born after implementation of <b><i>BaseManger Class</i></b> for future features and design patterns
