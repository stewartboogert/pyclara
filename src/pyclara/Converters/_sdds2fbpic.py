import numpy as np

def sdds2fbpic(sddsfile) :
    xbeam = np.array(sddsfile.getColumnValueList("x"))
    ybeam = np.array(sddsfile.getColumnValueList("y"))
    xpbeam = np.array(sddsfile.getColumnValueList("xp"))
    ypbeam = np.array(sddsfile.getColumnValueList("yp"))
    dtbeam = np.array(sddsfile.getColumnValueList("dt"))
    pbeam = np.array(sddsfile.getColumnValueList("p"))
    pxbeam = xpbeam * pbeam
    pybeam = ypbeam * pbeam

    

    return {"x" : xbeam, "y" : ybeam, "xp" : xpbeam, "yp" : ypbeam, "dt" : dtbeam, "p" : pbeam, "px" : pxbeam, "py" : pybeam}

    
    