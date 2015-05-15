Treepy is a python library for programmatic interaction with tree.mu.

To install treepy, clone this repo first::

    $ git clone https://github.com/ianalis/treepy.git

then run `setup.py`::

    $ python setup.py install

Here is an example session::

    >>> from treepy.client import TreeClient
    >>> client = TreeClient()
    >>> results = client.get_most_correlated('Flu')
    >>>
    >>> from treepy.utils import results_to_dframe
    >>> results_df = results_to_dframe(results)
    >>> results_df[:10]
    p_bh_double        p_bh_left  p_bh_right  p_double  p_left  p_right  \
    0            0  11496246.000000           0         0       1        0   
    1            0   5748123.000000           0         0       1        0   
    2            0   3832082.000000           0         0       1        0   
    3            0   2874061.500000           0         0       1        0   
    4            0   2299249.200000           0         0       1        0   
    5            0   1916041.000000           0         0       1        0   
    6            0   1642320.857143           0         0       1        0   
    7            0   1437030.750000           0         0       1        0   
    8            0   1277360.666667           0         0       1        0   
    9            0   1149624.600000           0         0       1        0   

            r                                        title  
    0  1.000000                                          Flu  
    1  0.867797                                         H5N1  
    2  0.863096                        Social_impact_of_H5N1  
    3  0.851355                                          Pig  
    4  0.843641                             Influenzavirus_A  
    5  0.842281                                     Bird_flu  
    6  0.831595                        Global_spread_of_H5N1  
    7  0.824759                        To_kill_a_mockingbird  
    8  0.823189  Table_of_books_of_Judeo-Christian_Scripture  
    9  0.821132           Transmission_and_infection_of_H5N1  
    >>>
    >>> from treepy.plotting import plot_corr
    >>> import matplotlib.pyplot as plt
    >>> plot_corr(results)                                                                                                                                                            
    <matplotlib.axes._subplots.AxesSubplot object at 0x7f28caec3750>                                                                                                                  
    >>> plt.show()
    >>>

For more information, see docstrings.