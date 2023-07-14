**A python lib to run ejabberd XML-RPC commands**

**Features**
<ul>
    <li>Execute XML-RPC commands</li>
    <li>External authentication</li>
    <li>Register Users</li>
    <li>Delete Users</li>
    <li>Create Rooms</li>
    <li>Subscribe to Rooms</li>
    <li>Send Messages</li>
    <li> and many others features, ... .</li>
</ul>

#### How to install
When working with python its a common approach to use a virtualenv to encapsulate all dependencies.
First create a virtual environment:
__if you have virtualenv installed run this code__
```python
virtualenv ejabberd_python3d_venv
```
__if not, so install with this code:__
````python
pip install virtualenv
````
and then install **ejabberd_python3d** lib:
```python
pip install ejabberd_python3d
```

To get the most updated version, you'll need to clone this repository:
````git
git clone http://github.com/Dedaldino3D/ejabberd_python3d.git
````
Run
````python
python setup.py
````

After installation is completed, create a client instance:

````python
from ejabberd_python3d.client import EjabberdAPIClient

client = EjabberdAPIClient('localhost','dedaldino','123456')
users = client.registered_users('localhost')
# assuming that you have an user registered (the admin) 
print(users) # [dedaldino]
client.register('dedaldino3d','localhost','nopassword')
users = client.registered_users('localhost')
print(users) # ['dedaldino3d']
````

