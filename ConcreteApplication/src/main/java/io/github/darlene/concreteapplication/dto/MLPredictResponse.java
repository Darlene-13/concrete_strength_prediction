package io.github.darlene.concreteapplication.dto;
import com.fasterxml.jackson.annotation.JsonFormat;

import lombok.Data;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;


/**
 * Data Transfer Object representing the raw prediction response
 * received from the FastAPI ML service.
 *
 * <p>Deserializes the snake_case JSON response from FastAPI
 * into a Java object using {@code @JsonProperty} field mappings.
 * This object is consumed by the service layer which maps it
 * into a {@link PredictionResponse} to return to the client.</p>
 *
 * <p>This class intentionally has no validation annotations —
 * it receives data from a trusted internal ML service,
 * not from an external client.</p>
 *
 * @author Darlene
 * @version 1.0
 * @see MLPredictionRequest
 * @see PredictionResponse
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class MLPredictionResponse {

    /**
     * Predicted compressive strength of the concrete mix in MPa.
     * Deserialized from {@code "predicted_strength_mpa"} in FastAPI response.
     */
    @JsonProperty("predicted_strength_mpa")
    private Double predictedStrengthMpa;

    /**
     * Identifier of the ML model version that produced this prediction.
     * Deserialized from {@code "model_version"} in FastAPI response.
     * Used for audit trail and model versioning.
     */
    @JsonProperty("model_version")
    private String modelVersion;

    /**
     * Status of the prediction returned by the ML service.
     * Deserialized from {@code "status"} in FastAPI response.
     * Expected value is {@code "success"} on successful prediction.
     */
    @JsonProperty("status")
    private String status;
}