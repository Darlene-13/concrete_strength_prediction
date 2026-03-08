package io.github.darlene.concreteapplication.client;

// Spring web client imports
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

//Spring annotations
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;

// Jackson annotation
import com.fasterxml.jackson.annotation.JsonProperty;

// DTO
import io.github.darlene.concreteapplication.dto.ConcreteRequest;

// Lombok
import lombok.extern.slf4j.Slf4j;

import lombok.Data;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Component  // Registers this as a spring bean - injectible everywhere
@Slf4j      // gives us log.info(), log.error() for free via lombok
public class MLServiceClient {




}
