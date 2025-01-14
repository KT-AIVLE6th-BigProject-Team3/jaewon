package com.aivle6team3.bigProject.client.api;

import com.aivle6team3.bigProject.client.dto.NoticeContent;
import com.aivle6team3.bigProject.client.dto.NoticeListResponse;
import com.aivle6team3.bigProject.client.dto.QnaContent;
import com.aivle6team3.bigProject.client.dto.QnaListResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@FeignClient(name = "fastApiClient", url = "${bigProject.api.host}")
public interface FastApiClient {

    // FastAPI 서버에서 처리할 실제 엔드포인트
    @GetMapping("/board/notice/list")
    public List<NoticeListResponse> getNoticeList(@RequestParam("page") int page, @RequestParam("limit") int limit);

    @GetMapping("/board/notice/content/{id}")
    public NoticeContent getNoticeContent(@PathVariable("id") int id);

    @GetMapping("/board/qna/list")
    public List<QnaListResponse> getQnaList(@RequestParam("page") int page, @RequestParam("limit") int limit);

    @GetMapping("/board/qna/content/{id}")
    public QnaContent getQnaContent(@RequestParam("id") int id);
}
