wavelength=RefractiveIndexINFO(:,1)*1000*1e-9;
n_exp=RefractiveIndexINFO(:,2);
k_exp=RefractiveIndexINFO(:,3);
omega=2*pi*3e8./wavelength;

epinf=5.90157;
%eps=5.90157*(1-wd^2/(x^2-1i*x*wd)-wl^2/(x^2-w0^2-1j*x*gammal))
% sqrt((abs(5.90157*(1-wd^2/(x^2-1i*x*gammad)-wl^2/(x^2-w0^2-1j*x*gammal)))+real(5.90157*(1-wd^2/(x^2-1i*x*gammad)-wl^2/(x^2-w0^2-1j*x*gammal))))/2)

%5339184710361415.0
%41082440000000.0 
%1993271708830714.8 
%4298305000000000.0 
%82084880000000.0