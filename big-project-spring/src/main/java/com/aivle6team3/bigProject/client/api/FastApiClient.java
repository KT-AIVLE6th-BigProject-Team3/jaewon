package com.aivle6team3.bigProject.client.api;

import com.aivle6team3.bigProject.client.dto.NoticeListResponse;
import com.aivle6team3.bigProject.client.dto.QnaListResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@FeignClient(name = "fastApiClient", url = "${bigProject.api.host}")
public interface FastApiClient {

    // FastAPI 서버에서 처리할 실제 엔드포인트
    @GetMapping("/board/notice")
    public List<NoticeListResponse> getNoticeList(@RequestParam("skip") int skip, @RequestParam("limit") int limit);

    @GetMapping("/board/qna")
    public List<QnaListResponse> getQnaList(@RequestParam("skip") int skip, @RequestParam("limit") int limit);
}
