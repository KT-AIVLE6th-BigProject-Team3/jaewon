package com.aivle6team3.bigProject.client.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class NoticeListResponse {
    private int notice_id;
    private String title;
    private String date;
    private String writer_id;
    private String content;
}
