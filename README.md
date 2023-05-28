The program is based on image encryption using chaos cryptography. And various security analysis 
is used to perform this project on chaos cryptography. 
 Run python Diff.py to check differential analysis
 Run python key_sensitivity_analysis.py to know about key sensitivity analysis results.
 Run python contrast_analysis.py to get contrast analysis results.
 Run python shanon_entro.py to get shanon entropy related results.
 Run python timer.py to get time analysis results.
 The differential analysis the cipher images are used to obtain plain text using differential attack and NPCR , UACI values are used for estimation
 In the key sensitivity analysis a plain text image will be encrypted using 2 key values and encrypted images will be obtained.Then the mathing pixel percentage
 is calculated.
 In contrast analysis, a graycomatrix is used and how much each pixel differ is calculated and then contrast at each angle is calculated and then
 average is calculated.
 In shanon entropy it deals with 8 bit images so the value obtained for shanon entropy should be close to 8 and hence obtain uniformity in cipher image pixels.
 In time analysis time for encryption to decryption is calculated for different algorithms like 2dlscm,pwlcm,logistic,lscml.
