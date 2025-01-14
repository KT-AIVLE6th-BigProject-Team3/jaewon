package com.aivle6team3.bigProject.client.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class QnaListResponse {
    public int id;              // QnA 게시글 번호
    public String title;            // 제목
    public String content;          // 작성내용(질문)
    public int user_id;        // QnA 작성자 ID
    public LocalDateTime created_at;             // QnA 작성일
    public LocalDateTime updated_at;             // QnA 수정일
    public int reply_user;
    public String reply_title;
    public String reply_content;
//    public LocalDateTime reply_at;
}
