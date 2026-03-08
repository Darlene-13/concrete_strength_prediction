package io.github.darlene.concreteapplication.dto;


import com.fasterxml.jackson.annotation.JsonProperty;


import lombok.Data;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object representing the outgoing prediction request
 * sent to the FastAPI ML service.
 *
 * <p>Carries the same concrete mix quantities as {@link ConcreteRequest}
 * but serializes field names to snake_case using {@code @JsonProperty}
 * to conform to the FastAPI service JSON contract.</p>
 *
 * <p>This class intentionally has no validation annotations —
 * all validation is handled upstream in {@link ConcreteRequest}
 * before this object is constructed by the service layer.</p>
 *
 * <p>Separating this DTO from {@link ConcreteRequest} decouples
 * the client-facing API contract from the ML service contract,
 * allowing each to evolve independently.</p>
 *
 * <p>All quantities are in kg/m³ except age which is in days.</p>
 *
 * @author Darlene
 * @version 1.0
 * @see ConcreteRequest
 * @see MLPredictionResponse
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class MLPredictRequest {

    /**
     * Cement content in kg/m³.
     * Serialized as {@code "cement"} in the ML service request body.
     */
    @JsonProperty("cement")
    private Double cement;

    /**
     * Blast furnace slag content in kg/m³.
     * Serialized as {@code "blast_furnace_slag"} in the ML service request body.
     * Zero indicates mix does not use slag.
     */
    @JsonProperty("blast_furnace_slag")
    private Double blastFurnaceSlag;

    /**
     * Fly ash content in kg/m³.
     * Serialized as {@code "fly_ash"} in the ML service request body.
     * Zero indicates mix does not use fly ash.
     */
    @JsonProperty("fly_ash")
    private Double flyAsh;

    /**
     * Water content in kg/m³.
     * Serialized as {@code "water"} in the ML service request body.
     */
    @JsonProperty("water")
    private Double water;

    /**
     * Superplasticizer content in kg/m³.
     * Serialized as {@code "superplasticizer"} in the ML service request body.
     * Zero indicates mix does not use superplasticizer.
     */
    @JsonProperty("superplasticizer")
    private Double superplasticizer;

    /**
     * Coarse aggregate content in kg/m³.
     * Serialized as {@code "coarse_aggregate"} in the ML service request body.
     */
    @JsonProperty("coarse_aggregate")
    private Double coarseAggregate;

    /**
     * Fine aggregate content in kg/m³.
     * Serialized as {@code "fine_aggregate"} in the ML service request body.
     */
    @JsonProperty("fine_aggregate")
    private Double fineAggregate;

    /**
     * Curing age of the concrete in days.
     * Serialized as {@code "age"} in the ML service request body.
     */
    @JsonProperty("age")
    private Integer age;
}