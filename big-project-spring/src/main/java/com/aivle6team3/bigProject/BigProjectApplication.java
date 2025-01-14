package com.aivle6team3.bigProject;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class BigProjectApplication {

	public static void main(String[] args) {
		SpringApplication.run(BigProjectApplication.class, args);
	}

}
