package com.aivle6team3.bigProject.client.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class QnaListResponse {
    public int qna_id;              // QnA 게시글 번호
    public String writer_id;        // QnA 작성자 ID
    public String date;             // QnA 작성일
    public String content;          // 작성내용(질문)
    public String title;            // 제목
    public String answer_id;        // 답변자 ID(관리자)
    public String answer_content;   // 답변 내용
}
