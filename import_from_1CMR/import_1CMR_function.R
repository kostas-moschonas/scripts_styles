import_from_1CMR <- function(relative_file_path, 
                             df_name =  "volumes_df",
                             output_path = paste(df_name, ".csv", sep = "")
                             ){
  # Script to import separete csv files and clean them into a dataframe. 
  # Unless specified, the df will be called "volumes_df" and stored in your working directory
  # Valid format on 1CMR output on 15/9/2024
  
  # Ensure those libraries are already loaded
  # library(tidyverse)
  # library(readr)
  
  # read & import csv files
  file_pattern <- "^MHCM\\d+.*\\.csv$"  # Regular expression for file pattern
  csv_files <- list.files(path = relative_file_path , pattern = file_pattern)
  
  # combine csv files into a list
  data_list <- lapply(csv_files, function(file) {
    path <- file.path(relative_file_path, file) 
    
    df <- read_csv(path)
    df$Scan_Date <- as.numeric(df$Scan_Date)   
    df$Analysis_Date <- as.numeric(df$Analysis_Date) 
    return(df)
  })
  
  # Combine the dataframes
  combined_df <- bind_rows(data_list)
  
  # remove unwanted columns
  combined_df <-  combined_df |> select(- Patient_ID,
                                        - Patient_DoB,
                                        - LGE,
                                        - Cardiac_Native_T1,
                                        - Cardiac_ECV,
                                        - Liver_Native_T1,
                                        - Liver_ECV,
                                        - Spleen_Native_T1,
                                        - Spleen_ECV,
                                        - T2)
  
  # change date format
  combined_df$Scan_Date <- as.Date(as.character(combined_df$Scan_Date), format = "%Y%m%d")
  combined_df$Analysis_Date <- as.Date(as.character(combined_df$Analysis_Date), format = "%Y%m%d")
  
  # change column names
  combined_df <-  combined_df |> 
    rename(record_id = Patient_Name,
           date_cmr = Scan_Date,
           date_analysis = Analysis_Date,
           lvedv = LVEDV,
           lvesv = LVESV,
           sv = LVSV,
           lvef = LVEF,
           mass = LVM_Mass,
           mwt = MWT,
           lv_length = LV_Length,
           lvedv_tr = trLVEDV,
           lvesv_tr = trLVESV,
           sv_tr = trLVSV,
           lvef_tr = trLVEF,
           mass_tr = trLVM_Mass,
           rvedv = RVEDV,
           rvesv = RVESV,
           rvsv = RVSV,
           rvef = RVEF,
           mapse_lat = MAPSE_Lat,
           mapse_sep = MAPSE_Sep,
           tapse = TAPSE,
           la_area = LA_Area,
           ra_area = RA_Area)

  # clean environment from intermediate objects
  rm(csv_files,
     file_pattern,
     data_list)
  
  # save as csv. Unless specified, it will save in your working directory
  write.csv(combined_df, output_path, row.names = FALSE)
}

   