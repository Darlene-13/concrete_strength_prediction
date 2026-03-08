package io.github.darlene.concreteapplication.dto;


import com.fasterxml.jackson.annotation.JsonFormat;

import lombok.Getter;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * Data Transfer Object representing the response returned to the client
 * after a successful concrete compressive strength prediction.
 *
 * <p>Carries the predicted strength value, model metadata and a timestamp.
 * This object is constructed by the service layer after receiving
 * the prediction from the ML service and is never persisted directly.</p>
 *
 * <p>Designed to be minimal — contains only what the client needs
 * to act on the prediction result.</p>
 *
 * @author Darlene
 * @version 1.0
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class PredictionResponse {

    /**
     * Predicted compressive strength of the concrete mix in MPa.
     * Returned directly from the XGBoost ML model via the FastAPI service.
     */
    private Double predictedStrengthMpa;

    /**
     * Identifier of the ML model version that produced this prediction.
     * Used for audit trail and model versioning tracking.
     */
    private String modelVersion;

    /**
     * Status of the prediction request.
     * Returns "success" on successful prediction.
     * Returns error description if prediction failed.
     */
    private String status;

    /**
     * Timestamp of when this prediction was generated.
     * Formatted as yyyy-MM-dd HH:mm:ss for readability.
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime timestamp;
}