### Cheat Sheet(Test-Driven Development with Python - O'Reilly Media)

ref: http://chimera.labs.oreilly.com/books/1234000000754/index.html


#### Chapter 1. Getting Django Set Up Using a Functional Test  
1) Obey the Testing Goat.  

    $ git rm -r --cached superlists/__pycache__  
    $ echo “*.pyc” >> .gitignore  
  
  
#### Chapter 2. Extending Our Functional Test Using the unittest Module  
1) Functional Test = Acceptance Test = End-to-End Test  
2) assertEqual, assertTrue, assertFalse  
3) User Story, Expected failure  
  
  
#### Chapter 3. Testing a Simple Home Page with Unit Tests  
1) Functional Test for User / Unit Test for Programmer  
2) Unit test for view  
  
    $ git log --oneline  
  
  
#### Chapter 4. What Are We Doing with All These Tests?  
1) For the tomorrow. just obey the Testing Goat.  
2) Refactoring : code improving without the result  
3) test process  

    writing test
    if pass test:
        if needn't refactoring:
            goto writing test
    writing min code
  
  
#### Chapter 5. Saving User Input  
1) POST request  
2) csrf(Cross-Site Request Forgery)  
3) Red (code fail) -> Green (min code) -> Refactor (.. removing dup) and Triangulation  
4) code smell, Three strikes and Refactor  
5) django ORM  
6) redirection after POST  
7) each tests for only a function  
8) job note  
  
    $ python3 manage.py makemigration  
    $ python3 manage.py migrate  
  
  
#### Chapter 6. Getting to the Minimum Viable Site  
1) Agile - gradual steps  
2) YAGNI(You Ain’t Gonna need It)  
3) django - assertTemplateUsed  
4) refactoring cat  
  
    $ python3 manage test # both  
    $ python3 manage test functional_tests # FT  
    $ python3 manage.py test lists # UT  
    $ pip3 install --upgrade selenium  
    $ grep -E “class|def” lists/tests.py  
  
  
#### Chapter 7. Prettification: Layout and Styling, and What to Test About It  
1) bootstrap - jumbotron  
2) django template  
3) static files, LiveServerTestCase  
  
    $ git reset --hard  
    $ python3 manage.py collectstatic # STATIC_ROOT  
  
  
#### Chapter 8. Testing Deployment Using a Staging Site  
1) mail to obeythetestinggoat@gmail.com  
2) ssh-key gen: https://www.linode.com/docs/networking/ssh/use-public-key-authentication-with-ssh/  
3) set server env (nginx, virtualenv)  
  
    server$ export SITENAME=dsa-test-staging.astinchoi.com  
    server$ mkdir -p ~/sites/$SITENAME/database, static, virtualenv, source  
    server$ git clone https://github.com/AstinCHOI/book_tdd_django ~/sites/$SITENAME/source  
    $ virtualenv --python=python3 ../virtualenv  
    $ source ../virtualenv/bin/activate  
    (virtualenv)$ pip install django  
    (virtualenv)$ pip freeze > requirements.txt  
    (virtualenv)$ deactivate  

    # in server virtualenv  
    server$ ../virtualenv/bin/pip install -r requirements.txt  
    server$ sudo vim /etc/nginx/sites-available/dsa-test-staging.astinchoi.com  
    server {
        listen 80;
        server_name dsa-test-staging.astinchoi.com;

        location / {
          proxy_pass http://localhost:8000;
        }
    }

    server$ sudo ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME  
    server$ sudo rm /etc/nginx/sites-enabled/default  
    server$ sudo service nginx reload  
    server$ ../virtualenv/bin/python3 manage.py runserver  
    $ python3 manage.py test functional_tests/ --liveserver=dsa-test-staging.astinchoi.com  
    server$ gunicorn superlists.wsgi:application  
    server$ ../virtualenv/bin/python3 manage.py collectstatic --noinput  
    server$ ls ../static/  
    server$ sudo vim /etc/nginx/sites-available/dsa-test-staging.astinchoi.com  
    server {
        listen 80;
        server_name dsa-test-staging.astinchoi.com;
      
        location /static {
            alias /home/ubuntu/sites/ dsa-test-staging.astinchoi.com/static;
        }
    
        location / {
            proxy_pass http://localhost:8000;
        }
      }
  
    server$ sudo service nginx reload  
    server$ gunicorn superlists.wsgi:application  
    $ python3 manage.py test functional_tests/ --liveserver=dsa-test-staging.astinchoi.com  
    server$ sudo vim /etc/nginx/sites-available/dsa-test-staging.astinchoi.com  
    server {
        listen 80;
        server_name dsa-test-staging.astinchoi.com;

        location /static {
        alias /home/ubuntu/sites/dsa-test-staging.astinchoi.com/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/dsa-test-staging.astinchoi.com.socket;
      }
    }
  
    server$ sudo service nginx reload  
    server$ gunicorn --bind unix:/tmp/dsa-test-staging.astinchoi.com.socket superlists.wsgi:application  
    $ python3 manage.py test functional_tests/ --liveserver=dsa-test-staging.astinchoi.com  
    server$ vim superlists/settings.py    
    ...
    DEBUG = FALSE
    ALLOWED_HOSTS = ['dsa-test-staging.astinchoi.com']

    server$ sudo vim /etc/init/gunicorn-dsa-test-staging.astinchoi.com.conf  
    description "Gunicorn server for dsa-test-staging.astinchoi.com"

    start on net-device-up
    stop on shutdown

    respawn

    setuid ubuntu
    chdir /home/ubuntu/sites/dsa-test-staging.astinchoi.com/source

    exec ../virtualenv/bin/gunicorn \
        --bind unix:/tmp/dsa-test-staging.astinchoi.com.socket \
        superlists.wsgi:application
  
    $ sudo start gunicorn-dsa-test-staging.astinchoi.com
  
4) Provisioning  
- suppose that there are user account and home folder
- apt-get install nginx git python-pip
- pip install virtualenv
- nginx setting for virtual host
- upstart setting for gunicorn
  
5) Deployment  
- create directory structure to ~/sites
- save the source to source folder
- start virtualenv at ../virtualenv
- pip install -r requirements.txt
- python manage.py migrate ...
- python manage.py collectstatic ...
- settings.py DEBUG=False, ALLOWED_HOSTS setting
- restart gunicorn
- check it through FT
  

#### Chapter 9. Automating Deployment with Fabric
1) https://github.com/AstinCHOI/book_tdd_django/blob/ch9/deploy_tools/fabfile.py
  
    $ fab deploy:host=ubuntu@dsa-test-staging.astinchoi.com -i {private_key}
    $ fab deploy:host=ubuntu@dsa-test.astinchoi.com -i {private_key}
    (if hostname CNAMEd to CDN, use /etc/hosts)

    server$ sed "s/SITENAME/dsa-test.astinchoi.com/g" \
    deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/dsa-test.astinchoi.com
    server$ sudo ln -s /etc/nginx/sites-available/dsa-test.astinchoi.com /etc/nginx/sites-enabled/dsa-test.astinchoi.com
    server $ sed "s/SITENAME/dsa-test.astinchoi.com/g" \
    deploy_tools/gunicorn-upstart.template.conf | sudo tee /etc/init/gunicorn-dsa-test.astinchoi.com.conf
  
    $ git tag LIVE
    $ export TAG=`date +DEPLOYED-%F/%H%M`
    $ echo $TAG
    $ git tag $TAG
    $ git push origin LIVE $TAG
    $ git log --graph --oneline --decorate
  

#### Chapter 10. Input Validation and Test Organisation
1) from unittest import skip  
2) split functional & unit tests  
3) dunderinit(double-undersocre) : \__init__.py  
4) with self.assertRaises(ValidationError):  
5) item.full_clean() # check the validation manually  
6) http://getbootstrap.com/css/#forms  
7) https://docs.djangoproject.com/en/1.9/topics/http/urls/#reverse-resolution-of-urls  
8) https://docs.djangoproject.com/en/1.9/topics/http/shortcuts/#redirect  
9) get_absolute_url(), redirect()  
  
  
#### Chapter 11. A Simple Form
1) https://django-crispy-forms.readthedocs.org/  
2) http://bit.ly/1rR5eyD  
3) Thin view >> django form  
4) Each test should test one thing  
5) Use helper function  
  
    $ grep id_new_item functional_tests/test*
    $ grep -r id_new_item lists/
    $ grep -Ir item_text lists
  

#### Chapter 12. More Advanced Forms
1) An Aside on When to Test for Developer Stupidity  
2) class Meta:  
https://docs.djangoproject.com/en/1.9/ref/models/options/  
3) assertQuerysetEqual  
4) model validation  
https://docs.djangoproject.com/en/1.9/ref/models/instances/#validating-objects  
5) form validation  
https://docs.djangoproject.com/en/1.9/ref/forms/validation/  

    $ python3 manage.py test functional_tests.[file_name]
    $ python3 manage.py test functional_tests.[file_name].[class].[function]

#### Chapter 13. Dipping Our Toes, Very Tentatively, into JavaScript
1) Setting Up a Basic JavaScript Test Runner  
- http://qunitjs.com/
- ref: https://mochajs.org/
2) javascript syntax check tool  
- jslint, jshint
3) jQuery namespace $  
http://api.jquery.com/ready/  
  
  
#### Chapter 14. Deploying Our New Code
    pass
  

#### Chapter 15. User Authentication, Integrating Third-Party Plugins, and Mocking with JavaScript  
1) Mozilla Persona (BrowserID)  
2) Spiking  
- check new API or new solution  
- prototype check  
http://stackoverflow.com/questions/249969/why-are-tdd-spikes-called-spikes  
3) customising authentication  
https://docs.djangoproject.com/en/1.9/topics/auth/customizing/
4) de-spiking  
- rewrite prototype code using tdd  
5) Mocking  
- unit test for external service.  
- simulation for external API.  
https://mockmyid.com/  
http://personatestuser.org/  
6) selenium - WebDriverWait (explicit wait)  
http://docs.seleniumhq.org/docs/04_webdriver_advanced.jsp  
https://code.google.com/p/selenium/source/browse/py/selenium/webdriver/support/wait.py  
7) javascript namespace : require.js  
8) stub, mock, fake, spy  
https://leanpub.com/mocks-fakes-stubs  
9) sinon.js mock  
- especially help to ajax test
http://sinonjs.org/  
10) QUnit setup and teardown, Testing Ajax  
http://sinonjs.org/docs/#server  
http://api.jquery.com/jQuery.post/  
11) javascript deferred  
http://otaqui.com/blog/1637/introducing-javascript-promises-aka-futures-in-google-chrome-canary/  
  

#### Chapter 16. Server-Side Authentication and Mocking in Python
1) from unites.mock ..  
2) django authentication(user login)  
https://docs.djangoproject.com/en/1.9/topics/auth/default/#how-to-log-a-user-in  
3) django session, cookie, authentication  
    $ python3 manage.py
    In [1]: from django.contrib.sessions.models import Session
    # browser - sessionid
    In [2]: session = Session.objects.get(session_key="bu5nd23qvs0mftq7qfkj5uc31r1j766w")
    In [3]: print(session.get_decoded())
4) python unittest magicMock  
5) django get_user method  
http://bit.ly/SuECDa  
5) python mock library  
6) patch decorator  
  
  
#### Chapter 17. Test Fixtures, Logging, and Server-Side Debugging
1) Text fixture (dangerous)  
setting up database by test data  
http://bit.ly/1kSTyrb  
https://factoryboy.readthedocs.org/  
2) De-duplicate your FTs, but don't skip too much  
3) text fixture : precondition before test  
4) retain from json fixture -> use ORM or tools like factory_boy  
5) Fixtures also have to work remotely  
6) Use loggers named after the module you’re in  
7) Test important log messages  
  
    $ sudo restart gunicorn-dsa-test-staging.astinchoi.com
  

#### Chapter 18. Finishing “My Lists”: Outside-In TDD
1) Outside in : outer (GUI) to inner code, like we did (TDD)  
- Programming by wishful thinking
2) Inside out : sub to upper component, common  
3) @property decorator..  
implement easily duck typing  
  

#### Chapter 19. Test Isolation, and “Listening to Your Tests”
1) functional test : user view / slow feed-back period / no help to simple code  
2) Integrated tests (depending on ORM or test clients) : fast, easy / know integration issue / not drive to good design (up to you) / slow than isolated test (usually)  
3) Isolated (mocky) tests : hard job / hard understandable / drive good design code / fast  
  

#### Chapter 20. Continuous Integration (CI)
1) Jenkins  
- Set up CI as soon as possible for your project
    server$ wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
    server$ echo deb http://pkg.jenkins-ci.org/debian binary/ | sudo tee \
    /etc/apt/sources.list.d/jenkins.list
    server$ sudo apt-get update
    server$ sudo apt-get install jenkins
    server$ sudo apt-get install git firefox python3 python-virtualenv xvfb

2) Jenkins Plugin  
- Git, ShiningPanda, Xvfb plugin  
- Xvfb (X Virtual FrameBuffer and ref: pyvirtualdisplay)  
- Set up screenshots and HTML dumps for failures  
https://wiki.jenkins-ci.org/display/JENKINS/Xvfb+Plugin  
http://manpages.ubuntu.com/manpages/trusty/man1/xvfb-run.1.html  
http://blog.martin-lyness.com/archives/installing-xvfb-on-ubuntu-9-10-karmic-koala  
server$ sudo aptitude install x11-xkb-utils  
server$ sudo aptitude install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic  
server$ sudo aptitude install xserver-xorg-core  
server$ sudo aptitude remove dbus  
server$ xvfb-run firefox  
  

3) QUnit javascript test  
- install node.js
    $ npm install -g phantomjs
http://qunitjs.com/plugins/ (https://github.com/jonkemp/qunit-phantomjs-runner)  

- run test
    $ phantomjs superlists/static/tests/runner.js lists/static/tests/tests.html
    $ phantomjs superlists/static/tests/runner.js accounts/static/tests/tests.html
  
    server$ sudo apt-get update
    server$ sudo apt-get install nodejs
    server$ sudo npm install -g phantomjs
  
4) implicitly_wait, not stable can use find_element. Use wait_for  
5) CI with staging, not production  
  
  
#### Extra. Command in need
1) git  
    $ git branch {branch_name}
    $ git branch -d {branch_name}
    $ git checkout -b {branch_name}
    $ git checkout master
    $ git merge {branch_name}
    $ git push origin master
  
2) view log  
    $ tail -f /var/log/nginx/error.log

3) view process  
    $ ps aux | grep gunicorn
    $ ps -eAf | grep -i xvfb
  
4) ubuntu AWS account password login activation  
    ubuntu$ sudo passwd ubuntu
    ubuntu$ sudo vim /etc/ssh/sshd_config
    PasswordAuthentication yes
    ubuntu$ sudo reload ssh
  
5) disk amount  
    $ df -h
    $ du -sk {path}

6) port check  
    $ netstat -tnlp
    $ nmap localhost