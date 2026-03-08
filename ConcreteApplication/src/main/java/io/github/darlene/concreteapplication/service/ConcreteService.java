package io.github.darlene.concreteapplication.service;

import io.github.darlene.concreteapplication.client.MLServiceClient;
import io.github.darlene.concreteapplication.dto.ConcreteRequest;
import io.github.darlene.concreteapplication.dto.MLPredictResponse;
import io.github.darlene.concreteapplication.dto.PredictionResponse;
import io.github.darlene.concreteapplication.entity.PredictionRecord;
import io.github.darlene.concreteapplication.repository.PredictionRepository;

import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Service layer for concrete strength prediction business logic.
 * Orchestrates the ML service call, database persistence
 * and response construction.
 *
 * @author Darlene
 * @version 1.0
 */
@Service
@Slf4j
public class ConcreteService {

    private final MLServiceClient mlServiceClient;
    private final PredictionRepository predictionRepository;

    public ConcreteService(MLServiceClient mlServiceClient,
                           PredictionRepository predictionRepository) {
        this.mlServiceClient = mlServiceClient;
        this.predictionRepository = predictionRepository;
    }

    /**
     * Orchestrates a concrete strength prediction:
     * calls ML service, persists record, returns response.
     *
     * @param request validated concrete mix ingredients
     * @return PredictionResponse with predicted strength and metadata
     */
    public PredictionResponse predict(ConcreteRequest request) {

        log.info("Received prediction request: {}", request);

        // Call ML service
        MLPredictResponse mlResponse = mlServiceClient.predict(request);

        // Build and save entity
        PredictionRecord record = PredictionRecord.builder()
                .cement(request.getCement())
                .blastFurnaceSlag(request.getBlastFurnaceSlag())
                .flyAsh(request.getFlyAsh())
                .water(request.getWater())
                .superplasticizer(request.getSuperplasticizer())
                .coarseAggregate(request.getCoarseAggregate())
                .fineAggregate(request.getFineAggregate())
                .age(request.getAge())
                .predictedStrength(mlResponse.getPredictedStrengthMpa())
                .modelVersion(mlResponse.getModelVersion())
                .build();

        predictionRepository.save(record);
        log.info("Prediction saved to database with id: {}", record.getId());

        // Build and return response
        return PredictionResponse.builder()
                .predictedStrengthMpa(mlResponse.getPredictedStrengthMpa())
                .modelVersion(mlResponse.getModelVersion())
                .status(mlResponse.getStatus())
                .timestamp(LocalDateTime.now())
                .build();
    }

    /**
     * Retrieves all prediction records ordered by most recent first.
     *
     * @return list of all prediction records
     */
    public List<PredictionRecord> getAllPredictions() {
        return predictionRepository.findAllByOrderByCreatedAtDesc();
    }

    /**
     * Retrieves a single prediction record by id.
     *
     * @param id prediction record id
     * @return PredictionRecord if found
     * @throws RuntimeException if no record found with given id
     */
    public PredictionRecord getPredictionById(Long id) {
        return predictionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Prediction not found"));
    }
}