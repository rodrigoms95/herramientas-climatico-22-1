PIB = true
SSP = "SSP5"

if PIB
    fname_d = "GDP_SSP_SPATIAL13R.mat";
    fname_r = "GDP_" + SSP + ".nc";
    var = "GDP";
    mat = load(fname_d);
    mx = flip(mat.GDPMX, 1);
else
    fname_d = "POP_SSP_SPATIAL13R.mat";
    fname_r = "POP_" + SSP + ".nc";
    var = "POP";
    mat = load(fname_d);
    mx = flip(mat.POPMX, 1);
end

nccreate(fname_r, var,...
    "Dimensions",...
    {"lat",360,"lon",720,"time",91});
ncwrite(fname_r, var, mx);