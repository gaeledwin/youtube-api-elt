import logging

logger = logging.getLogger(__name__)
table = 'api_elt'

def insert_row(cur, conn, schema, row):
    try:
        logger.info("Insert row process....")
        if schema == "staging":
            video_id = "video_id"
            cur.execute(f"""
                INSERT INTO {schema}.{table}("Video_Id", "Video_Title", "Uploads_Date", "Duration", "View_Count", "Like_Count", "Comment_Count")
                VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);
            """, row
            )
        else:
            video_id = "Video_Id"
            cur.execute(f"""
                INSERT INTO {schema}.{table}("Video_Id", "Video_Title", "Uploads_Date", "Duration", "View_Count", "Like_Count", "Comment_Count", "Type")
                VALUES (%(Video_Id)s, %(Video_Title)s, %(Uploads_Date)s, %(Duration)s, %(View_Count)s, %(Like_Count)s, %(Comment_Count)s, %(Type)s);
            """, row
            )
        conn.commit()
    except Exception as e:
        logger.error(f'Error insert row : {row[video_id]} - {e}')
        conn.rollback()  
        raise e  
        
def update_row(cur, conn, schema, row):
    try:
        if schema == "staging":
            video_id = "video_id"
            video_title = "title"
            uploads_date = "publishedAt"
            view_count = "viewCount"
            like_count = "likeCount"
            comment_count = "commentCount"
            cur.execute(f"""
            UPDATE {schema}.{table}
            SET "Video_Title" = %({video_title})s, "View_Count" = %({view_count})s, "Like_Count" = %({like_count})s, "Comment_Count" = %({comment_count})s
            WHERE "Video_Id" = %({video_id})s and "Uploads_Date" = %({uploads_date})s;
                    """, row)
        else:
            video_id = "Video_Id"
            video_title = "Video_Title"
            uploads_date = "Uploads_Date"
            view_count = "View_Count"
            like_count = "Like_Count"
            comment_count = "Comment_Count"
        
            cur.execute(f"""
                UPDATE {schema}.{table}
                SET "Video_Title" = %({video_title})s, "View_Count" = %({view_count})s, "Like_Count" = %({like_count})s, "Comment_Count" = %({comment_count})s, "Type"=%(Type)s
                WHERE "Video_Id" = %({video_id})s and "Uploads_Date" = %({uploads_date})s;
                    """, row)
        conn.commit()
    except Exception as e:
        logger.error(f'Updated row {row[video_id]}')
        raise e
    
def delete_row(conn, cur, schema, ids):
    try:
        formatted_ids = ", ".join(f"'{id}'" for id in ids)
        ids_str = f"({formatted_ids})"
        request = f"""DELETE FROM {schema}.{table} WHERE "Video_Id" in {ids_str}"""
        cur.execute(request)
        conn.commit()
    except Exception as e:
        logger.error(f"error to delete id: {ids}")
        raise e
