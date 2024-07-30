


# Un used Functions


# def get_file_created_time(uploaded_file):
#     # Save the uploaded file temporarily to access its metadata
#     with open(uploaded_file.name, "wb") as f:
#         f.write(uploaded_file.getbuffer())
    
#     # Get the absolute path of the saved file
#     file_path = os.path.abspath(uploaded_file.name)
    
#     created_time = os.path.getctime(file_path)
#     created_time_dt = datetime.utcfromtimestamp(created_time)
#     sri_lanka_tz = pytz.timezone('Asia/Colombo')
#     japan_tz = pytz.timezone('Asia/Tokyo')
#     created_time_utc = pytz.utc.localize(created_time_dt)
#     created_time_sl = created_time_utc.astimezone(sri_lanka_tz)
#     created_time_jp = created_time_sl.astimezone(japan_tz)
    
#     # Clean up the temporary file
#     os.remove(file_path)
    
#     return created_time_jp
