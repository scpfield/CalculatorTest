===============================================================================
                       Google Calculator Test Client

-------------------------------------------------------------------------------
                               OVERVIEW
-------------------------------------------------------------------------------

The test client is a Python program that communicates with the Chrome (or 
MSEdge) web browser to perform UI functional testing of Google's Calculator app.

It uses the Chrome CDP Protocol to locate and interact with the UI Elements of 
the calculator.  Communication between the test client and Chrome is done 
through an asynchronous WebSocket connection.

CDP Reference:

https://chromedevtools.github.io/devtools-protocol/

Chrome CDP has a large set of functionality, much of it is very useful for QA 
Testing.  For the purposes of this small test client, it is only using the 
following CDP functions:

Target.attachToTarget:
https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-attachToTarget

Target.setAutoAttach:
https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-setAutoAttach

Page.navigate:
https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-navigate

Runtime.evaluate:
https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-evaluate

Runtime.getProperties:
https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-getProperties

Runtime.callFunctionOn:
https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-callFunctionOn

DOM.getDocument:
https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getDocument

DOM.requestChildNodes:
https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-requestChildNodes

DOM.describeNode:
https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-describeNode

DOM.resolveNode:
https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-resolveNode

DOM.getContentQuads:
https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getContentQuads

Accessibility.queryAXTree:
https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/#method-queryAXTree

Input.dispatchMouseEvent:
https://chromedevtools.github.io/devtools-protocol/tot/Input/#method-dispatchMouseEvent

Browser.close:
https://chromedevtools.github.io/devtools-protocol/tot/Browser/#method-close

The test client enables event notifications for nearly all the CDP Domains, but 
for this small test, it is only using one async browser event:

Accessibility.loadComplete:
https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/#event-loadComplete


-------------------------------------------------------------------------------
                               INSTALL
-------------------------------------------------------------------------------

Installation pre-requirements:

1.  A recent / latest version of Chrome web browser.

2.  A recent Python version:  Either 3.11.x or 3.12.x

3.  The following Python packages (and their dependencies, usually installed 
    automatically by pip):

    requests
    websocket-client
    argparse
    psutil
    deprecated

There is a "Py-CDP" python package that is bundled with the test client, and 
does not need to be installed separately.  It contains a series of Python 
classes that perform serialization + deserialization of the CDP Protocol 
commands from Python Objects to JSON, to be transmitted over the WebSocket 
wire connection.

Please forgive me if I have neglected/forgotten to include any other python 
requirements.


3.  Unzip CalculatorTest.zip into a suitable location.

4.  From a command prompt, run the CalculatorTest.py file with a "--help" 
    argument, which will help to verify all pre-requirement packages are 
    installed:
    
    $ python3 CalculatorTest.py --help
    
If there are missing packages it should throw a bunch of errors indicating 
which ones are missing.  If not, you should see a help summary.

The only parameter that is necessary is the "--binary" argument which tells 
CalculatorTest where to find Chrome, if it is not in the $PATH.

Examples:

    for linux:
    
    $ python3 CalculatorTest.py --binary /usr/bin/google-chrome
    
    for windows:
    
    C:> python3 CalculatorTest.py --binary "C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    
If you are running the test client for the first time, it is recommended 
to use the following speed parameter to slow down the speed of the automation.  
Otherwise, it runs so fast it may be difficult to visualize what it is doing.

    $ python CalculatorTest.py --speed slow
    

The test client and Chrome should not need root-level privileges, but YMMV.

Brief description of the files in the .zip:


CalculatorTest.py
-----------------
The main file used to run the automation. It has most of the high-level 
functionality for running the test cases, calling the CDP functions for 
locating elements, sending mouse-clicks, etc.  It has a simple Page class, 
Element class, Button class, and a Tester class.
 
 
ChromeLauncher.py
-----------------
This file contains a class for launching Chrome with customized parameters.  
It will automatically kill any currently-running Chrome browser processes 
prior to launching a new Chrome instance.  Once a new Chrome is launched, it 
does an initial HTTP connection to the browser on a special internal URL which 
provides the WebSocket URLs that are used to connect to the CDP interface.
 
 
ChromeClient.py
---------------
This file contains a class that provides the "Engine" to communicate with 
Chrome. It establishes the WebSocket connection, and provides easy-to-use 
interface for invoking Chrome CDP functions and receiving async browser events.
 
 
CDPDataWrappers.py
------------------
This file contains classes for encapsulating the response information from the 
 Chrome CDP function calls and Events, to provide an easy-to-use interface.
 
 
Util.py
-------
Miscellaneous helper functions.


The sub-directory: cdp 
----------------------
The PyCDP classes which do the Object-To-JSON serialization + deserialization 
of the CDP Protocol commands.


TestData.txt
------------
This file contains the actual test cases that will be executed on the 
calculator app, such as:

"1 + 1"
 
Please open and read the comments in that file.  It describes the tests in more 
detail.  

Feel free to add your own tests!


-------------------------------------------------------------------------------
                               RUNNING THE TESTS
-------------------------------------------------------------------------------

The test cases defined in the file: TestData.txt are referred to by the 
test client as "Static Tests".  That is because they are not dynamically 
generated test cases.

When any test case is run, the test client begins to click the buttons on 
the calculator.  For every button that is clicked, it reads the calculator's 
Display to verify it shows the correct value.

For example, if the test case is:  "123 + 456"

First it clicks the "1" button, and checks the Display to verify "1" is
displayed.

Then it clicks the "2" button, and checks the Display to verify "12" is
displayed.

Then it clicks the "3" button, and checks the Display to verify "123" is
displayed.

And so on.  Parenthesis in test cases are supported.

Once the entire test case is entered into the calculator, the final step
is clicking the "Equals" button, which makes the calculator app perform the
calculation and display the result in the Display.

The result from the calculator app is compared to the result of the same
calculation performed by the Python interpreter / evaluator.  This is done 
to cross-check the result from Google's calculator to, minimally, at least
one other "known-good" calculator.  

Currently the test client is in "interactive" mode, so it will prompt the
user to press [Enter] before each test case is run.

Other tests included:

CE Button-specific test case.
Randomized / Dynamic test cases.


-------------------------------------------------------------------------------
                        GENERATING RANDOM TEST CASES
-------------------------------------------------------------------------------

Running the test client with the parameter:

   $ python3 CalculatorTest.py --generate-random-tests 100

This will generate 100 random permutations of test cases.  The number is how 
many to generate.  

One example:


(-25056.67) - ((-60576) - 49878.421 - 35545.347 - ((-3083.02138387) + 59430 / 39263) / (-40384)) * ((-18891.1019) * 2587.99384214 - (-8029.8668) / (5361 / ((-42513.95) - 41350.2690536 / ((-61213.701297)))))
                        

They can be copy/pasted into the TestData.txt file if desired.  

The test client also generates random tests by itself dynamically.


-------------------------------------------------------------------------------
                            UNFINISHED WORK
-------------------------------------------------------------------------------

Due to time, I was not able to finish the design + implementation of a number
of important items:


1.  A well-defined, structured format for describing the tests that were
    executed, and the pass/fail results.  Currently it only prints the results
    to the console.
    
    If this were a real test client, it would be very important to have a 
    proper mechanism for reporting test results.  In particular, in a format 
    that is designed to be consumed by a CI/CD module.
    
    It is also very important for any test client to clearly differentiate
    between a failure of the software being tested vs. a failure of the test
    client itself.
    
2.  Additional error-handling.  There are many places in the code that needs
    more robust handling of all sorts of potential failure scenarios.
    
3.  Even though numbers are pretty much universal, likely there are 
    Localization / Internationalization test cases to be written.

4.  Performance testing. Javascript CPU usage, memory usage, etc.  One of 
    the neat capabilities of the Chrome CDP is it gives you programmatic 
    access to all of the same Performance monitors and tools that the 
    normal GUI DevTools provides.
    
5.  Keyboard input for the automation.  Chrome CDP provides a 
    "dispatchKeyEvent" function similar to dispatching Mouse events.  
    I simply ran out of time.
    
    
-------------------------------------------------------------------------------
                             END OF README
-------------------------------------------------------------------------------
