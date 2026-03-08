package io.github.darlene.concreteapplication.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;

import jakarta.validation.Valid;

import io.github.darlene.concreteapplication.dto.ConcreteRequest;
import io.github.darlene.concreteapplication.dto.PredictionResponse;
import io.github.darlene.concreteapplication.entity.PredictionRecord;
import io.github.darlene.concreteapplication.service.ConcreteService;

import lombok.extern.slf4j.Slf4j;

import java.util.List;

/**
 * REST controller for concrete compressive strength prediction endpoints.
 *
 * <p>Handles all incoming HTTP requests under {@code /api/v1/concrete}.
 * Responsible only for HTTP concerns — request mapping, input validation,
 * response wrapping and logging. All business logic is delegated
 * to {@link ConcreteService}.</p>
 *
 * <p>Endpoints exposed:
 * <ul>
 *   <li>POST /api/v1/concrete/predict — submit a mix for prediction</li>
 *   <li>GET  /api/v1/concrete/predictions — retrieve all predictions</li>
 *   <li>GET  /api/v1/concrete/predictions/{id} — retrieve by id</li>
 * </ul>
 * </p>
 *
 * @author Darlene
 * @version 1.0
 */
@RestController
@RequestMapping("/api/v1/concrete")
@Slf4j
@Validated
public class ConcreteController {

    private final ConcreteService concreteService;

    /**
     * Constructs ConcreteController with required service dependency.
     *
     * @param concreteService service layer handling prediction logic
     */
    public ConcreteController(ConcreteService concreteService) {
        this.concreteService = concreteService;
    }

    /**
     * Accepts a concrete mix design and returns the predicted
     * compressive strength from the ML service.
     *
     * <p>Input is validated via {@code @Valid} before reaching
     * the service layer. Invalid requests are rejected with 400 Bad Request.</p>
     *
     * @param request validated concrete mix ingredients from request body
     * @return 200 OK with {@link PredictionResponse} containing
     *         predicted strength, model version, status and timestamp
     */
    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predict(
            @RequestBody @Valid ConcreteRequest request) {
        log.info("Received predict request: {}", request);
        PredictionResponse response = concreteService.predict(request);
        return ResponseEntity.ok(response);
    }

    /**
     * Retrieves all concrete strength prediction records
     * ordered by most recent first.
     *
     * @return 200 OK with list of all {@link PredictionRecord} entities
     */
    @GetMapping("/predictions")
    public ResponseEntity<List<PredictionRecord>> getAllPredictions() {
        log.info("Fetching all predictions...");
        return ResponseEntity.ok(concreteService.getAllPredictions());
    }

    /**
     * Retrieves a single prediction record by its database id.
     *
     * @param id the unique identifier of the prediction record
     * @return 200 OK with the matching {@link PredictionRecord}
     * @throws RuntimeException if no record exists with the given id
     */
    @GetMapping("/predictions/{id}")
    public ResponseEntity<PredictionRecord> getPredictionById(
            @PathVariable Long id) {
        log.info("Fetching prediction with id: {}", id);
        return ResponseEntity.ok(concreteService.getPredictionById(id));
    }
}