% the routine compares two files with corresponding numbers inside. It calculates
% the maximum error and the mean of all the errors.

% If it is run without arguments, specify the following two paths
% f0_path = "../results-sw.txt"
% f1_path = "../approxResults-hw.txt"

function calcErr (f0_path, f1_path) 

err = 0;
meanErr = 0;
maxErr = 0;

delimiter = {''};
formatSpec = '%f%[^\n\r]';
fileID0 = fopen(f0_path,'r');
fileID1 = fopen(f1_path,'r');
dataArray0 = textscan(fileID0, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN,  'ReturnOnError', false);
dataArray1 = textscan(fileID1, formatSpec, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN,  'ReturnOnError', false);
fclose(fileID0);
fclose(fileID1);
resultsSW = dataArray0{:, 1};
approxResultsHW = dataArray1{:, 1};
clearvars f0_path f1_path delimiter formatSpec dataArray0 dataArray1 fileID0 fileID1 dataArray ans;

for i = 1 : numel(resultsSW)
    err = resultsSW(i) - approxResultsHW(i);
    meanErr = meanErr + err;
    if (abs(err) > abs(maxErr))
        maxErr = err;
    end
end

meanErr = meanErr / numel(resultsSW);

end