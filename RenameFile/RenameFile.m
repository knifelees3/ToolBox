% The files saved from comsol has bad expressions of variavles and we need rename them
folder='../SimulationFile/solutions/';
file_struct=dir(folder);
Data_Cell=struct2cell(file_struct);
file_list=Data_Cell(1,:)';
file_list(1:2)=[];
num_files=length(file_list);  


for l=1:num_files
    file=file_list{l};
    var_m=regexp(file,'[\d\.]*\dE\-\d','match');
    if length(var_m)~=0
    var_nm=num2str(str2num(var_m{1})*1e9,'%03.f');
    var_before=regexp(file,'[A-Za-z_]*_','match');
    new_name=[folder,var_before{:},var_nm,'nm.mph'];
    old_name=[folder,file];
    movefile(old_name,new_name);
    end
end