# Run

``
python method_otsu.py input.jpg output.png
``

## Example

``
python method_otsu.py Image_processing_pre_otsus_algorithm.jpg output.png
``


python -m cProfile -s tottime method_otsu.py Image_processing_pre_otsus_algorithm.jpg output.png
         473308 function calls (465785 primitive calls) in 2.100 seconds

Ordered by: internal time
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    1.591    1.591    1.591    1.591 method_otsu.py:7(otsu)


python -m cProfile -s tottime method_otsu.py Image_processing_pre_otsus_algorithm.jpg output.png 
         473356 function calls (465833 primitive calls) in 2.067 seconds

Ordered by: internal time
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    1.561    1.561    1.561    1.561 method_otsu.py:7(otsu)
