import sys, os, builtins, signal, io, operator, gc, ctypes, tracemalloc, linecache
import inspect, threading, json, random, copy, time, threading, traceback
from functools import wraps


def GetExceptionInfo( e ):
    ExceptionInfo = ''.join(traceback.format_exception(e))
    return(ExceptionInfo)


def RandomString(Length=10):
    RandBytes = bytearray(Length)
    for x in range(Length):
        RandBytes[x] = random.randrange(65,91)
    return(RandBytes.decode().replace(" ", "_").lower())

def Pause( Text = None ):

    try:
        if Text == None:
            Text = "Pausing"

        Data = input(Text)

        if Data and len(Data) > 0:
            if Data[0] == 'q':
                os._exit(0)
    except BaseException as Failure:
        ...



# This is a Python Annotator I wrote to 
# measure how much memory a Python function uses.
    
def CheckMemory( TargetFunction ):

    @wraps( TargetFunction )
    def FunctionWrapper( *args, **kwargs ):

        # first, run full GC to clear everything it can
        gc.collect()

        # start the tracemalloc with 25 traceback frame history
        tracemalloc.start( 25 )

        # clear all prior trace data and reset peak data
        tracemalloc.clear_traces()
        tracemalloc.reset_peak()

        # before calling target function, get the current
        # traced memory info that should be a decently clean state

        # get_traced_memory() returns a tuple of 2 ints
        # representing bytes. I wanted megabytes so divide them
        # by 1024*1000 and round to 2 digits.

        MB = 1024 * 1000

        HeapSize, PeakSize = tracemalloc.get_traced_memory()
        HeapSize = round( HeapSize / MB, 4)
        PeakSize = round( PeakSize / MB, 4)

        print()
        print("------------------------------------------------------")
        print( f"Before calling        : {TargetFunction.__name__}" )
        print( f"Current Heap Size MB  : {HeapSize}")
        print( f"Peak Heap Size MB     : {PeakSize}" )
        print("------------------------------------------------------")
        print()

        # take the "before" tracemalloc snapshot
        Snapshot1  =  tracemalloc.take_snapshot()

        # run GC again just before calling function
        gc.collect()

        # call target function
        ReturnValue  =  TargetFunction( *args, **kwargs )

        # run GC again just after function returns
        gc.collect()

        # take the "after" tracemalloc snapshot
        Snapshot2  =  tracemalloc.take_snapshot()

        HeapSize, PeakSize = tracemalloc.get_traced_memory()
        HeapSize = round( HeapSize / MB, 4)
        PeakSize = round( PeakSize / MB, 4)

        print()
        print("------------------------------------------------------")
        print( f"After calling         : {TargetFunction.__name__}" )
        print( f"Current Heap Size MB  : {HeapSize}")
        print( f"Peak Heap Size MB     : {PeakSize}" )

        # get diff stats from snapshots
        SnapshotDiff = Snapshot2.compare_to(
                                 Snapshot1,
                                 key_type = 'lineno' )

        # stop tracemalloc
        tracemalloc.stop()

        print()
        print( "Top Heap Differences:" )
        print()

        TotalDiff = 0.0

        for Idx, Stat in enumerate( SnapshotDiff[:5], 1 ):

            Frame       = Stat.traceback[0]
            DiffSize    = round( Stat.size_diff / MB, 4 )
            File        = Frame.filename.split( os.sep )[-1]
            Line        = Frame.lineno
            Code        = linecache.getline( File, Line ).strip()
            TotalDiff   += Stat.size_diff

            print(f"{Idx}: Size: {DiffSize} MB, " +
                  f"File: {File}, Line: {Line}, " +
                  f"Code: \"{Code}\"")

        TotalDiff = round( TotalDiff / MB, 4 )

        print()
        print(f"Total: {TotalDiff} MB")
        print()
        print("------------------------------------------------------")
        print()
        return ReturnValue
    return FunctionWrapper
    ...



