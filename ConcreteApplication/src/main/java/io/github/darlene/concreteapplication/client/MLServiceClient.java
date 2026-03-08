package io.github.darlene.concreteapplication.client;

import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;

import io.github.darlene.concreteapplication.dto.ConcreteRequest;
import io.github.darlene.concreteapplication.dto.MLPredictRequest;
import io.github.darlene.concreteapplication.dto.MLPredictResponse;

import lombok.extern.slf4j.Slf4j;

@Component  // Registers this as a spring bean - injectible everywhere
@Slf4j      // gives us log.info(), log.error() for free via lombok
public class MLServiceClient {

    private final WebClient webClient;
    @Value("${ml.service.url}")
    private String mlServiceUrl;


    public MLServiceClient(WebClient.Builder webClientBuilder){
        this.webClient = webClientBuilder.build();
    }
    //Predict method signature
    /**
     * Calls the FastAPI ML service with the concrete mix ingredients
     * and returns the predicted compressive strength.
     *
     * @param request validated concrete mix from the controller
     * @return MLPredictResponse containing predicted strength and metadata
     * @throws RuntimeException if the ML service is unreachable
     */
    public MLPredictResponse predict(ConcreteRequest request){

        // Builder mapping..
        MLPredictRequest mlRequest = MLPredictRequest.builder()
                .cement(request.getCement())
                .blastFurnaceSlag(request.getBlastFurnaceSlag())
                .flyAsh(request.getFlyAsh())
                .water(request.getWater())
                .superplasticizer(request.getSuperplasticizer())
                .coarseAggregate(request.getCoarseAggregate())
                .fineAggregate(request.getFineAggregate())
                .age(request.getAge())
                .build();
        // Log outgong call....
        log.info("Sending request to ML Service: {}", mlRequest);

        try {
            //STEP 3: CALL ML service
            MLPredictResponse response = webClient
                    .post()
                    .uri(mlServiceUrl + "/predict")
                    .bodyValue(mlRequest)
                    .retrieve()
                    .bodyToMono(MLPredictResponse.class)
                    .block();

            return response;
        } catch(WebClientResponseException e){

            // Log the error info
            log.error("Error calling ML Service: {}", e.getMessage());
            throw new RuntimeException("ML service unavailable");
        }
    }
}
