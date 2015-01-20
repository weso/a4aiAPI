var obs_indicators = [
		"ITU_A",
		"ITU_G",
		"ITU_K",
		"ITU_L",
		"ITU_O",
		"WB_A",
		"IEA_A",
		"WI_D",
		"Q1",
		"ITU_B",
		"ITU_J",
		"ITU_R",
		"ITU_S",
		"Q20",
		"WEF_B",
		"Q19",
		"Q18",
		"WI_C",
		"WI_B",
		"ITU_P",
		"Q42",
		"Q40",
		"Q41",
		"UN_B",
		"Q39",
		"Q38",
		"WB_H",
		"WB_D",
		"FH_A",
		"FH_B",
		"EIU_A",
		"WEF_A",
		"Q11",
		"Q10",
		"ODB.2013.C.RTI",
		"Q7",
		"RSF_A",
		"Q52",
		"ITU_N",
		"Q49",
		"SOCIAL_NETWORKS_A",
		"WI_F",
		"Q46",
		"Q47",
		"Q44",
		"Q45",
		"Q43",
		"UN_C",
		"Q15",
		"Q14",
		"Q16",
		"Q13",
		"ODB.2013.D1-D15",
		"WIKI_A",
		"Q3",
		"Q2",
		"Q5",
		"Q4",
		"EM_A",
		"ODB.2013.I.ENTR",
		"ODB.2013.C.SUPIN",
		"ODB.2013.I.GOV",
		"WEF_L",
		"Q17",
		"Q12",
		"ODB.2013.I.ECON",
		"Q9",
		"Q8",
		"INSEAD_A",
		"Q36",
		"UN_D",
		"Q33",
		"Q32",
		"Q31",
		"Q30",
		"Q37",
		"Q35",
		"Q34",
		"Q28",
		"Q29",
		"ODB.2013.I.ACCOUNT",
		"WEF_C",
		"Q51",
		"Q48",
		"Q50",
		"ODB.2013.I.INC",
		"ODB.2013.I.ENV",
		"Q6"
	];
	
var ind_indicators = [
"ITU_G",
		"WI_D",
		"ITU_A",
		"ITU_O",
		"WB_A",
		"IEAA",
		"ITU_K",
		"GSMA",
		"ITU_B",
		"WI_B",
		"WEF_B",
		"ITU_R",
		"ITU_S",
		"ITU_J",
		"A13",
		"UN_B",
		"WB_D",
		"UNDP/WB",
		"S13",
		"RSF_A",
		"WEF_A",
		"FH_A",
		"FHB",
		"P4",
		"P3",
		"P6",
		"P7",
		"P8",
		"P9",
		"S12",
		"WIKI_A",
		"UN_C",
		"ITU_N",
		"SOCIAL_NETWORKS_A",
		"S10",
		"S6",
		"C1",
		"WEF_L",
		"INSEAD_A",
		"S5",
		"I5",
		"I6",
		"P10",
		"UN_D",
		"WEF_C",
		"P2",
		"I1",
		"I2",
		"S1",
		"S2",
		"S3",
		"S4",
		"S7",
		"S8",
		"S9",
		"S11",
		"I4",
		"I3"
]

var deprecated = [];
var newOnes = [];
var permanent = [];

for (var i = 0; i < obs_indicators.length; i++) {
  var indicator = obs_indicators[i];
  
  if (ind_indicators.indexOf(indicator) == -1)
  	deprecated.push(indicator);
  else
    permanent.push(indicator);
}

for (var i = 0; i < ind_indicators.length; i++) {
  var indicator = ind_indicators[i];
  
  if (obs_indicators.indexOf(indicator) == -1)
  	newOnes.push(indicator);
}

console.log("DEPRECATED: " + deprecated.length);
console.log(deprecated);

console.log("NEW: " + newOnes.length);
console.log(newOnes);

console.log("PERMANENT: " + permanent.length);
console.log(permanent);