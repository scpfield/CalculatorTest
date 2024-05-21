import  sys, os, time, signal, random, json, websocket, ssl, socket, ctypes, cdp, argparse, decimal
from    ChromeLauncher import ChromeLauncher
from    ChromeClient   import *
from    Util import *


class CalculatorTest():

    def __init__(   self, 
                    CDP         = None, 
                    Speed       = None,
                    TestData    = None,
                    StrictMode  = None ):

        self.CDP        = CDP
        self.Speed      = Speed
        self.TestData   = TestData
        self.StrictMode = StrictMode
        
        self.StaticTests = []


    def InitializeCDP( self ):

        ReturnValue = self.CDP.ExecuteMethod( cdp.log.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.page.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.page.set_lifecycle_events_enabled, enabled = True )
        ReturnValue = self.CDP.ExecuteMethod( cdp.dom.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.dom_snapshot.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.dom_storage.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.debugger.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.runtime.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.css.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.accessibility.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.audits.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.inspector.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.overlay.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.profiler.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.performance.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.service_worker.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.layer_tree.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.media.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.console.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.database.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.animation.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.indexed_db.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.heap_profiler.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.security.enable )
        ReturnValue = self.CDP.ExecuteMethod( cdp.web_authn.enable )

        ReturnValue = self.CDP.ExecuteMethod( cdp.browser.get_version )
        ReturnValue.Print()
        
        return True

    def LoadTestData( self ):
    
        self.StaticTests = []
        
        try:
        
            with open( self.TestData ) as TestDataFile:
            
                Lines = TestDataFile.readlines()
                
                for Line in Lines:

                    if Line[0] == '#' : continue
                    if Line[0] == '\n': continue
                    
                    self.StaticTests.append( list( map( str, Line.strip().split())))


            print( f'Loaded {len(self.StaticTests)} test cases' )
            return True
            
        except BaseException as e:
        
            print( f'Failed to load test data from: {self.TestData}' )
            return False


    def CreatePythonEvalStr( self, TestCase ):
    
        EvalStr = ''
        for Item in TestCase: EvalStr += f'{Item} '
        return EvalStr.strip()
    
    
    def RunTests( self ):

        # Create a new instance of the Calculator Page
        
        Page = CalculatorPage( 'https://www.google.com/search?q=calculator', 
                                self.CDP )


        # Load test case data from file
        
        if not self.LoadTestData(): 
            return False
        

        # Initialize Chrome CDP
        
        if not self.InitializeCDP():
            return False


        # Navigate to the Calculator Page

        if not Page.NavigateToPage():
            return False


        # Initialize Page automation elements
        
        if not Page.InitializeElements():
            return False
        
       
        # Execute the static tests defined in the test data file
        
        Result = self.RunCalculatorTests( Page, 
                                          Title      = "Static", 
                                          TestCases  = self.StaticTests )


        # Execute CE Button test
        
        Result = self.RunCEButtonTest( Page )


        # Generate and execute 10 random test cases
        
        RandomTestCases = []
        
        for x in range(10):
            RandomTestCases.append( 
                list( map( str, CalculatorTest.GenerateRandomTestCase().strip().split())))
            
        
        Result = self.RunCalculatorTests( Page, 
                                          Title      = "Random", 
                                          TestCases  = RandomTestCases )

        print()
        print()
        print( '***** Tests complete. Sleeping. Hit Control-C to exit ******' )
        print()
        
        time.sleep(500000)
        


    #
    # This function verifies the Calculator Display value is correct.
    #
    # It is called after every mouse-click of any calculator button to
    # verify the Display accurately reflects what the user did.
    #
    
    def CheckDisplayValue( self, Page, ButtonValue ):

        if ButtonValue == 'CE':
        
            self.ExpectedDisplayValue = self.ExpectedDisplayValue[:-1]
            
            if self.ExpectedDisplayValue == '':
                self.ExpectedDisplayValue = '0'
                
        else:
        
            self.ExpectedDisplayValue  += ButtonValue

        ActualValue     = Page.GetDisplayValue()
        ExpectedValue   = str( self.ExpectedDisplayValue )
        
        NumLParens      = self.ExpectedDisplayValue.count( Page.ButtonLParen.Label )
        NumRParens      = self.ExpectedDisplayValue.count( Page.ButtonRParen.Label )
        
        if ( NumLParens - NumRParens ) > 0:
                            
            if len( ExpectedValue ) > 1:
        
                if (( ExpectedValue[-2]  !=    Page.ButtonLParen.Label )    and
                    ( ExpectedValue[-1]  in  [ Page.ButtonPlus.Label,
                                               Page.ButtonMinus.Label,
                                               Page.ButtonMultiply.Label,
                                               Page.ButtonDivide.Label ] )):
                                            
                        ExpectedValue += ' '
                    
            ExpectedValue += str( Page.ButtonRParen.Label * 
                                ( NumLParens - NumRParens ))

        if ActualValue != ExpectedValue:
        
            ResultStr = ( f'[Failed]  ' +
                          f'Actual Display: "{ActualValue}" != ' +
                          f'Expected Display: "{ExpectedValue}"' )

            print( ResultStr )
            return ( False, ResultStr )
            
        else:
        
            ResultStr = ( f'[Passed]  ' +
                          f'Actual Display: "{ActualValue}" == ' +
                          f'Expected Display: "{ExpectedValue}"' )

            print( ResultStr )
            
            return ( True, ResultStr )



    #
    # This is the main Calculator Test executor.
    # 
    # For a given test case, such as: "123 + 456"
    #
    # This function clicks the buttons: "1", "2", 3", "+", "4", "5", "6"
    #
    # After each button is clicked, it checks the Calculator Display value
    # to make sure it is showing the correct value along the way.
    #
    # After the test case is entered, the function clicks the "Equals"
    # button to perform the actual calculation.
    #
    # The function compares the calculation result to the same calculation
    # performed by the Python interpreter, so we can compare if there
    # are any discrepancies.
    #
    # After each test case, the AC button is used to reset the calculator 
    # display back to 0.  If that fails or if there were other failures,
    # a fallback attempt using the CE button is performed to clear the display.
    #
    

    def RunCalculatorTests( self, Page, Title = None, TestCases = None ):
    
        if not Page: return False
        
        print()
        
        for TestNum, TestCase in enumerate( TestCases ):

            Key = ''           
            print()
            print( f'Press [Enter] to run {Title} Test Case #{TestNum+1}' )
            print()
            input( Key )

            TitleStr = ( f'{Title} Test Case #{TestNum+1}: ' + 
                         f'"{self.CreatePythonEvalStr(TestCase)}"' )
                        
            print()
            print( '-' * len(TitleStr) )
            print( TitleStr )
            print( '-' * len(TitleStr) )
            print()
            print( f'User Input Tests:' )
            print()

            self.ExpectedDisplayValue = ''
            TestFailed = False
            
            for Idx, Item in enumerate( TestCase ):
            
                if Idx > 0:
                    if TestCase[Idx-1] != '(' :
                        self.ExpectedDisplayValue += ' '
                    
                for SubItem in Item:
                
                    match SubItem:
                    
                        case '0':
                            
                            if not Page.Button0.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button0.Label )[0]:
                                TestFailed = True
                                break

                        case '1':
                            
                            if not Page.Button1.Click( self.Speed ):
                                TestFailed = True
                                break
                                
                            if not self.CheckDisplayValue( Page, Page.Button1.Label )[0]:
                                TestFailed = True
                                break
                                
                        case '2':
                            
                            if not Page.Button2.Click( self.Speed ):
                                TestFailed = True
                                break
                                
                            if not self.CheckDisplayValue( Page, Page.Button2.Label )[0]:
                                TestFailed = True
                                break

                        case '3':
                            
                            if not Page.Button3.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button3.Label )[0]:
                                TestFailed = True
                                break

                        case '4':
                            
                            if not Page.Button4.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button4.Label )[0]:
                                TestFailed = True
                                break

                        case '5':
                            
                            if not Page.Button5.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button5.Label )[0]:
                                TestFailed = True
                                break

                        case '6':
                            
                            if not Page.Button6.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button6.Label )[0]:
                                TestFailed = True
                                break

                        case '7':
                            
                            if not Page.Button7.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button7.Label )[0]:
                                TestFailed = True
                                break

                        case '8':
                            
                            if not Page.Button8.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button8.Label )[0]:
                                TestFailed = True
                                break

                        case '9':
                            
                            if not Page.Button9.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.Button9.Label )[0]:
                                TestFailed = True
                                break

                        case '.':
                            
                            if not Page.ButtonPoint.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonPoint.Label )[0]:
                                TestFailed = True
                                break

                        case '+':
                            
                            if not Page.ButtonPlus.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonPlus.Label )[0]:
                                TestFailed = True
                                break

                        case '-' | '−':
                            
                            if not Page.ButtonMinus.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonMinus.Label )[0]:
                                TestFailed = True
                                break

                        case '*' | 'x' | '×':
                            
                            if not Page.ButtonMultiply.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonMultiply.Label )[0]:
                                TestFailed = True
                                break

                        case '/' | '÷':
                            
                            if not Page.ButtonDivide.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonDivide.Label )[0]:
                                TestFailed = True
                                break

                        case '(':
                            
                            if not Page.ButtonLParen.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonLParen.Label )[0]:
                                TestFailed = True
                                break
                                
                        case ')':
                            
                            if not Page.ButtonRParen.Click( self.Speed ):
                                TestFailed = True
                                break
                            
                            if not self.CheckDisplayValue( Page, Page.ButtonRParen.Label )[0]:
                                TestFailed = True
                                break
                                
                        case _ as Invalid:
                        
                            print( f'Invalid test case item: {Invalid}')
                            TestFailed = True
                            break
                
                # end of SubItem loop
                if TestFailed: break
            
            
            # finished entering user input
            # now click Equals to calculate result

            if not TestFailed:
            
                print()
                print( 'Calculation Accuracy Test:' )
                print()
                
                if not Page.ButtonEquals.Click( self.Speed ):
                    print( 'Failed to click Equals button' )
                    TestFailed = True
            
            
                CalculatorResult    = Page.GetDisplayValue()
                PythonEvalResult    = ''

                try:
                
                    # Run the same calculation we did with Google using
                    # the Python interpreter, so we can compare Google's result
                    # with another calculator.
                    
                    PythonEvalResult = eval( self.CreatePythonEvalStr( TestCase ))

                    # Of course there are inherently differences between the two
                    # calculators, StrictMode toggles how strict we want to be
                    # in flagging differences as test failures.
                    
                    if not self.StrictMode:
                    
                        # If Google's calculation is a float, count
                        # how many decimal digits it is
                        
                        GoogleDigits  = 0
                        GoogleEPower  = 0
                        
                        if '.' in CalculatorResult:
                        
                            ResultSplit = CalculatorResult.split('.')[1].split('e')
                            
                            if len( ResultSplit ) > 0:
                                GoogleDigits = len( str( ResultSplit[0] ))
                            
                            if len( ResultSplit) == 2:
                                GoogleEPower = int( ResultSplit[1] )
                                
                                                    
                        # If Google's result is an integer, and Python's 
                        # result is a float with ".0" as the decimal portion
                        # For example:  4  vs  4.0 
                        # Then convert the Python result to an integer so we 
                        # don't consider the comparison a failure.
                        
                        if GoogleDigits == 0:
                                                
                            if ( PythonEvalResult % 1 ) == 0:
                                PythonEvalResult = int( PythonEvalResult )

                        # Google returns results for floats rounded to 
                        # seemingly arbitrary lengths -- sometimes it is
                        # rounded to 10 digits, sometimes 11, sometimes 6.
                        # It never matches the Python rounding, and causes
                        # the comparisons to fail.
                        #
                        # So this rounds the Python result to the same 
                        # number of digits before comparison.
                        
                        if GoogleDigits > 0:
                            
                            PythonEvalResult = round( float(PythonEvalResult), GoogleDigits )
                            
                            if GoogleEPower > 0:
                                PythonEvalResult = format( PythonEvalResult, f'.{GoogleDigits+1}')
                                           
                    
                    PythonEvalResult = str( PythonEvalResult )
                                        
                except ( BaseException, Exception ) as e:
                
                    # If Python fails to calculate the test case,
                    # set the eval result to the string "Error" which is what
                    # Google uses to report when it fails to calculate
                    # print( GetExceptionInfo(e) )
                    PythonEvalResult = "Error"


                # Finally, do the comparison between Google's calculator
                # and Python's calculator.
                
                self.ExpectedDisplayValue = PythonEvalResult

                if not self.CheckDisplayValue( Page, '' )[0]:
                    TestFailed = True



            # Done with this test case, now attempt to reset 
            # the calculator for the next one

            print()
            print( 'Attempting to reset calculator display for the next test case' )
            print()
            
            if not Page.ButtonAllClear.Click( self.Speed ):
                TestFailed = True
                print( 'Failed to click AC Button to reset calculator display')

            self.ExpectedDisplayValue = '0'

            if not self.CheckDisplayValue( Page, '' )[0]:
                TestFailed = True
                print( 'Calculator is not reset to 0' )
            else:
                # Calculator is reset to 0, so continue with next test
                continue
                

            # Calculator is not reset to 0, so attempt to use the CE button 
            # to clear the display
            
            print()
            print( 'Attempting to clear display using CE Button' )
            print()
            
            DisplayValue = Page.GetDisplayValue()
            
            # Click the CE Button as many times as there are
            # items in the display to clear it
            
            for x in range( len( DisplayValue )):
            
                if not Page.ButtonClearEntry.Click( self.Speed ):
                    TestFailed = True
                    print( 'Failed to click CE Button' )
            

            # Check if the display is cleared (zeroed)
            
            self.ExpectedDisplayValue = '0'

            if not self.CheckDisplayValue( Page, '' )[0]:
            
                # Still unable to clear the display, so abort.
                
                TestFailed = True
                print( 'Unable to reset calculator to 0, exiting.' )
                return False
                
            else:
                # Display is cleared, continue onward
                continue


    #
    # This function is a separate test for the CE Button specifically.
    #
    # By default it adds 50 numbers to the Calculator Display,
    # then clicks the CE button 50 times to remove the numbers.
    #
    # Then repeats a few times.
    #
    
    def RunCEButtonTest( self, Page ):

        TitleStr = 'CE Button Test:'

        Key = ''
        
        print()
        print()
        print( 'Press enter to run the CE button test:' )
        print()
        input( Key )
                    
        print()
        print( '-' * len(TitleStr) )
        print( TitleStr )
        print( '-' * len(TitleStr) )
        print()

        TestFailed = False

        # repeat test 3 times
        
        for c in range( 3 ):
        
            # click the 9 button 50 times to fill the display
            
            self.ExpectedDisplayValue = ''
            
            for x in range( 50 ):

                if not Page.Button9.Click( Speed = 'fast' ):
                    print( 'Failed to click Button9' )
                    TestFailed = True

                if not self.CheckDisplayValue( Page, Page.Button9.Label )[0]:
                    TestFailed = True
                    return False

            # click the CE button 50 times to clear the display
            
            for x in range( 50 ):

                if not Page.ButtonClearEntry.Click( Speed = 'fast' ):
                    print( 'Failed to click CE Button' )
                    TestFailed = True

                if not self.CheckDisplayValue( Page, Page.ButtonClearEntry.Label )[0]:
                    TestFailed = True
                    return False

        if not TestFailed:  return True



    #
    # This function generates random permutations of test cases
    # with support for multiple nested parenthensis segments
    #

    @classmethod
    def GenerateRandomTestCase( self ):
    
        Operators       = '+-*/'
        MaxLength       = 200
        CurrentLength   = 0
        NumOpenParens   = 0
        TestCaseStr     = ''
        MinNumber       = -pow( 2, 16 )
        MaxNumber       =  pow( 2, 16 )
        MinFloatDigits  = 1
        MaxFloatDigits  = 10
        
        while CurrentLength < MaxLength:
        
            Operator = Operators[ random.randint( 0, (len(Operators) - 1) ) ]
            
            CoinFlip    = random.randint( 0, 1 )
            Number      = 0
            
            if CoinFlip:
                Digits  = random.randint( MinFloatDigits, MaxFloatDigits )
                Number  = round( random.uniform( MinNumber, MaxNumber), Digits )
            else:
                Number  = random.randint( MinNumber, MaxNumber )

            NumberStr       = str( Number )
            
            if Number < 0: 
                NumberStr   = f'({Number})'
                
            NumberStr       = f'{NumberStr} '
            Opened          = False
            CoinFlip        = random.randint( 0, 9 )
            
            if CoinFlip <= 3:
                Opened          = True
                NumOpenParens   += 1
                NumberStr       = f' ({NumberStr}'
            else:
                NumberStr       = f' {NumberStr}'
            
            if ((not Opened) and (NumOpenParens > 0)):
                
                CoinFlip        = random.randint( 0, 9 )
                
                if CoinFlip <= 3:
                    NumOpenParens  -= 1
                    NumberStr       = NumberStr.rstrip()
                    NumberStr       = f'{NumberStr}) '
                else:
                    NumberStr       = f'{NumberStr}'
            
            TestCaseStr     += NumberStr
            CurrentLength   = len(TestCaseStr)
                
            if ( CurrentLength >= MaxLength):
                
                TestCaseStr = TestCaseStr.rstrip()
                
                for x in range( NumOpenParens ):
                    TestCaseStr += ')'
                
            else:                                
                TestCaseStr += Operator
        
        return TestCaseStr.strip()
                 
            
        

#
# This is the Calculator Page class.
# 
# It keeps the buttons / elements for the page,
# and provides the methods:
#
#  InitializeElements
#  NavigateToPage
#  GetDisplayValue
#

class CalculatorPage():


    #
    # Basic constructor
    #
    # The CDP object is our Chrome Client
    # used to communicate with Chrome
    #
    
    def __init__( self, URL, CDP ):

        self.URL = URL
        self.CDP = CDP

        self.Button0            = None
        self.Button1            = None
        self.Button2            = None
        self.Button3            = None
        self.Button4            = None
        self.Button5            = None
        self.Button6            = None
        self.Button7            = None
        self.Button8            = None
        self.Button9            = None
        self.ButtonPoint        = None
        self.ButtonEquals       = None
        self.ButtonPlus         = None
        self.ButtonMinus        = None
        self.ButtonMultiply     = None
        self.ButtonDivide       = None
        self.ButtonLParen       = None
        self.ButtonRParen       = None
        self.ButtonAllClear     = None
        self.ButtonClearEntry   = None


    #
    # This invokes the Chrome CDP to make
    # the web browser go to the Calculator URL
    #
    # You will notice many calls to "CDP.ExecuteMethod".
    # It is our wrapper around the actual WebSocket calls.
    #
    
    def NavigateToPage( self ):

        if not self.URL: return False
        if not self.CDP: return False

        # Execute the CDP function to navigate to the Calculator URL
        # 
        # After the call returns, then we do a blocking wait
        # for an async notification from Chrome when the browser's
        # PageLoadCompleteEvent has occurred.
        
        ReturnValue = self.CDP.ExecuteMethod( cdp.page.navigate,
                                              url = self.URL )
                                              
        if ReturnValue.Error: return False
        
        print( 'CalculatorPage: Waiting for PageLoadCompleteEvent' )
        
        # We use a Python Event object to signal when Chrome
        # has delivered the PageLoadCompleteEvent
    
        self.CDP.WaitForEvent( self.CDP.PageLoadCompleteEvent )

        print( 'CalculatorPage: Got PageLoadCompleteEvent' )

        # After we receive notification, call the CDP function
        # to request the DOM document tree, because it forces
        # Chrome browser to get ready.
        
        ReturnValue = self.CDP.ExecuteMethod( cdp.dom.get_document,
                                              depth  = -1, 
                                              pierce = True )

        if ReturnValue.Error: return False
        
        self.DocumentNode = ReturnValue.CDPObject

        # Same reason as above
        
        ReturnValue = self.CDP.ExecuteMethod( cdp.dom.request_child_nodes,
                                              node_id = self.DocumentNode.node_id,
                                              depth   = -1, 
                                              pierce  = True )

        if ReturnValue.Error: return False

        # Navigation success
        
        return True
        
        
        

    def InitializeElements( self ):

        try:
        
            self.Button0            = Button(   Name     = '0',
                                                Locator  = { 'name' : '0', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button1            = Button(   Name     = '1',
                                                Locator  = { 'name' : '1', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button2            = Button(   Name     = '2',
                                                Locator  = { 'name' : '2', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button3            = Button(   Name     = '3',
                                                Locator  = { 'name' : '3', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button4            = Button(   Name     = '4',
                                                Locator  = { 'name' : '4', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button5            = Button(   Name     = '5',
                                                Locator  = { 'name' : '5', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button6            = Button(   Name     = '6',
                                                Locator  = { 'name' : '6', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button7            = Button(   Name     = '7',
                                                Locator  = { 'name' : '7', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button8            = Button(   Name     = '8',
                                                Locator  = { 'name' : '8', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.Button9            = Button(   Name     = '9',
                                                Locator  = { 'name' : '9', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonPoint        = Button(   Name     = 'point',
                                                Label    = '.',
                                                Locator  = { 'name' : 'point', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonEquals       = Button(   Name     = 'equals',
                                                Label    = '=',
                                                Locator  = { 'name' : 'equals', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonPlus         = Button(   Name     = 'plus',
                                                Label    = '+',
                                                Locator  = { 'name' : 'plus', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonMinus        = Button(   Name     = 'minus',
                                                Label    = '-',
                                                Locator  = { 'name' : 'minus', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonMultiply     = Button(   Name     = 'multiply',
                                                Label    = '×',
                                                Locator  = { 'name' : 'multiply', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonDivide       = Button(   Name     = 'divide',
                                                Label    = '÷',
                                                Locator  = { 'name' : 'divide', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonLParen       = Button(   Name     = 'left parenthesis',
                                                Label    = '(',
                                                Locator  = { 'name' : 'left parenthesis', 'role' : 'button' },
                                                CDP      = self.CDP )
                                                
            self.ButtonRParen       = Button(   Name     = 'right parenthesis',
                                                Label    = ')',
                                                Locator  = { 'name' : 'right parenthesis', 'role' : 'button' },
                                                CDP      = self.CDP )                                                

            self.ButtonAllClear     = Button(   Name     = 'all clear',
                                                Label    = 'AC',
                                                Locator  = { 'name' : 'all clear', 'role' : 'button' },
                                                CDP      = self.CDP )

            self.ButtonClearEntry   = Button(   Name     = 'clear entry',
                                                Label    = 'CE',
                                                Locator  = { 'name' : 'clear entry', 'role' : 'button' },
                                                CDP      = self.CDP )
        except BaseException as e:
            print( GetExceptionInfo(e) )
            return False
        
        return True
        

    def GetDisplayValue( self ):

        Script = 'document.querySelector(\'span[id="cwos"]\').innerText'

        ReturnValue = self.CDP.ExecuteScript( expression = Script, return_by_value = True )

        if ReturnValue.Error: return None

        Value = str(ReturnValue.Result.get('result').get('value'))

        return Value


class Element():

    def __init__(   self,
                    Name    = None,
                    Label   = None,
                    Locator = None,
                    CDP     = None  ):

        self.Locator    = Locator
        self.Name       = Name
        self.NodeID     = None
        self.ObjectID   = None
        self.CDP        = CDP
        self.Label      = Label

        if not self.Label: self.Label = Name

        self.UpperLeft  = ( None, None )
        self.UpperRight = ( None, None )
        self.LowerRight = ( None, None )
        self.LowerLeft  = ( None, None )
        self.Center     = ( None, None )


    def Locate( self ):

        ReturnValue     = self.CDP.ExecuteMethod( cdp.dom.get_document,
                                                  depth = 1, pierce = True )

        if ReturnValue.Error: return False

        DocumentNode    = ReturnValue.CDPObject

        ReturnValue     = self.CDP.ExecuteMethod( cdp.accessibility.query_ax_tree,
                                node_id         = DocumentNode.node_id,
                                accessible_name = self.Locator.get( 'name' ),
                                role            = self.Locator.get( 'role' ))

        if ReturnValue.Error: return False

        if not ReturnValue.Result.get('nodes'): return False

        self.NodeID     = ReturnValue.Result.get('nodes')[0].get('nodeId')

        ReturnValue     = self.CDP.ExecuteMethod( cdp.dom.resolve_node,
                                                  backend_node_id = cdp.dom.NodeId( self.NodeID ))

        if ReturnValue.Error: return False

        self.ObjectID   = ReturnValue.Result.get('object').get('objectId')

        if not self.GetContentQuads(): return False

        return True


    def GetContentQuads( self ):

        ReturnValue     = self.CDP.ExecuteMethod(
                            cdp.dom.get_content_quads,
                            object_id = cdp.runtime.RemoteObjectId( self.ObjectID ))

        if ReturnValue.Error: return False

        Quads           = ReturnValue.Result.get( 'quads' )[0]

        self.UpperLeft  = ( Quads[0], Quads[1] )
        self.UpperRight = ( Quads[2], Quads[3] )
        self.LowerRight = ( Quads[4], Quads[5] )
        self.LowerLeft  = ( Quads[6], Quads[7] )

        CenterX    = self.UpperLeft[0]  + (( self.UpperRight[0] - self.UpperLeft[0]  ) / 2 )
        CenterY    = self.LowerRight[1] + (( self.UpperRight[1] - self.LowerRight[1] ) / 2 )

        self.Center = ( CenterX, CenterY )

        return True

class Button( Element ):

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

    def Click( self, Speed = None ):

        if not self.Locate():   self.Located = False
        else:                   self.Located = True

        if not self.Located: return False

        if Speed == "slow": time.sleep(1)

        ReturnValue = self.CDP.ExecuteMethod( cdp.input_.dispatch_mouse_event,
                                              type_       = 'mousePressed',
                                              x           = self.Center[0],
                                              y           = self.Center[1],
                                              button      = cdp.input_.MouseButton(
                                                            cdp.input_.MouseButton.LEFT ),
                                              buttons     = 1,
                                              click_count = 1,
                                              timestamp = cdp.input_.TimeSinceEpoch( time.time() ))

        if ReturnValue.Error: return False

        ReturnValue = self.CDP.ExecuteMethod( cdp.input_.dispatch_mouse_event,
                                              type_       = 'mouseReleased',
                                              x           = self.Center[0],
                                              y           = self.Center[1],
                                              button      = cdp.input_.MouseButton(
                                                            cdp.input_.MouseButton.LEFT ),
                                              buttons     = 1,
                                              click_count = 1,
                                              timestamp = cdp.input_.TimeSinceEpoch( time.time() ))

        if ReturnValue.Error: return False

        return True


if __name__ == '__main__':

    ArgParser = argparse.ArgumentParser( argument_default    = True,
                                         add_help            = True,
                                         description         = 'CalculatorTest')

    ArgGroup  = ArgParser.add_argument_group()

    ArgGroup.add_argument(  '--binary',
                            required    = False,
                            action      = 'store',
                            default     = 'chrome',
                            help        = ( 'Full path + filename to the chrome or msedge binary,' +
                                            'or simply the filename if it exists in $PATH.  Default = "chrome".' +
                                            'On linux it might be named: "google-chrome"' ))

    ArgGroup.add_argument(  '--hostname',
                            required    = False,
                            action      = 'store',
                            default     = 'localhost',
                            help        = 'Hostname for Chrome to bind its WebSocket port.  Default = localhost' )

    ArgGroup.add_argument(  '--port',
                            required    = False,
                            action      = 'store',
                            type        = int,
                            default     = 9222,
                            help        = 'Listener port for Chrome.  Default = 9222' )

    ArgGroup.add_argument(  '--speed',
                            required    = False,
                            action      = 'store',
                            default     = 'fast',
                            help        = 'Speed of automation. Values either "fast" or "slow".  Default = "fast"' )

    ArgGroup.add_argument(  '--testdata',
                            required    = False,
                            action      = 'store',
                            default     = 'TestData.txt',
                            help        = 'Path + Filename for the test data file.  Default = TestData.txt' )

    ArgGroup.add_argument(  '--strict',
                            required    = False,
                            action      = 'store_true',
                            default     = False,
                            help        = 'Enable strict mode.  Default disabled.' )

    ArgGroup.add_argument(  '--generate-random-tests',
                            required    = False,
                            action      = 'store',
                            type        = int,
                            default     = 0,
                            help        = ( "Generate N random test cases. Doesn't run tests " +
                                            "just prints them to the console.\n" ))
    
                            

    Args    = ArgParser.parse_args()

    if Args.generate_random_tests:
    
        for x in range( Args.generate_random_tests ):
        
            print( CalculatorTest.GenerateRandomTestCase() )
            
        exit( 0 )


    Launcher = ChromeLauncher(  Args.binary,
                                Args.hostname,
                                Args.port )

    try:

        Client = ChromeClient( Launcher = Launcher )

    except ChromeClientException as e:

        print( GetExceptionInfo(e) )
        exit( 1 )

    Tester = CalculatorTest(    CDP        = Client, 
                                Speed      = Args.speed, 
                                TestData   = Args.testdata,
                                StrictMode = Args.strict )

    
    Tester.RunTests()

    Tester.CDP.CloseChrome()

    exit( 0 )
