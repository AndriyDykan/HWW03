dict_of_known_fileformat = {(".png", ".jpg", ".jpeg", ".svg"): "IMAGES",
                                         (".avi", ".mp4", ".mov", ".mkv"): "VIDEOS",
                                         (".mp3", ".ogg", ".wav", ".amr"): "AUDIO",
                                         (".gz", ".zip", ".tar"): "ARCHIVES",
                                         (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"): "DOCUMENTS", (): "UNKNOWN"
                                         }
print(dict_of_known_fileformat.get((".png")))