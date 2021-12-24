# Dispersion Model Fitting for Au

The following model will be used to fit the dispersion
$$
\varepsilon=\varepsilon_{inf}(1-\frac{\omega_{d}^2}{\omega^2-j\omega\omega_{d}}-\frac{\omega_{L}^2}{\omega^2-j\omega\gamma-\omega_{0}^2}
$$
The experimental data can be download from this website

[https://refractiveindex.info/](https://refractiveindex.info/)

I write a program use the `curve_fit` function from python to fit the Lorentzian shape.

![](C:\Users\xiail\Documents\Dropbox\Code\DipoleEmissionInSymmetricStructure\Dispersion_Fitting\ReadMe.assets\DispersionforAu.png)