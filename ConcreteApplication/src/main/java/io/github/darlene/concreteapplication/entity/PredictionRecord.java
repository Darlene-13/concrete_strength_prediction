package io.github.darlene.concreteapplication.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Column;
import jakarta.persistence.GenerationType;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

import org.hibernate.annotations.CreationTimestamp;
import java.time.LocalDateTime;

import lombok.Getter;
import lombok.Setter;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

/**
 * Entity representing a single concrete strength prediction record.
 *
 * <p>Maps to the {@code prediction_record} table in the database.
 * Each record captures the full concrete mix design submitted by the client,
 * the predicted compressive strength returned by the ML service,
 * and metadata about when the prediction was made.</p>
 *
 * <p>Validation is applied at both the DTO layer (incoming request)
 * and here at the entity layer (before database persistence)
 * following defense-in-depth principles.</p>
 *
 * @author Darlene
 * @version 1.0
 */

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "prediction_record")

public class PredictionRecord {

    /**
     * Auto-generated primary key.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Cement content in kg/m³.
     * Primary binder — required in all concrete mixes.
     */
    @NotNull
    @Positive
    @Column(name = "cement")
    private Double cement;

    /**
     * Water content in kg/m³.
     * Required for hydration — directly affects w/c ratio and strength.
     */
    @NotNull
    @Positive
    @Column(name = "water")
    private Double water;

    /**
     * Blast furnace slag content in kg/m³.
     * Optional supplementary cementitious material (SCM).
     * Zero indicates mix does not use slag.
     */
    @PositiveOrZero
    @Column(name = "blast_furnace_slag")
    private Double blastFurnaceSlag;

    /**
     * Fly ash content in kg/m³.
     * Optional supplementary cementitious material (SCM).
     * Zero indicates mix does not use fly ash.
     */
    @PositiveOrZero
    @Column(name = "fly_ash")
    private Double flyAsh;

    /**
     * Superplasticizer content in kg/m³.
     * Optional chemical admixture that improves workability
     * and allows reduction of water content.
     * Zero indicates mix does not use superplasticizer.
     */
    @PositiveOrZero
    @Column(name = "superplasticizer")
    private Double superplasticizer;

    /**
     * Coarse aggregate content in kg/m³.
     * Forms the structural skeleton of the concrete mix.
     * Required in all mixes.
     */
    @NotNull
    @Positive
    @Column(name = "coarse_aggregate")
    private Double coarseAggregate;

    /**
     * Fine aggregate (sand) content in kg/m³.
     * Fills voids between coarse aggregate particles.
     * Required in all mixes.
     */
    @NotNull
    @Positive
    @Column(name = "fine_aggregate")
    private Double fineAggregate;

    /**
     * Curing age in days at time of strength measurement.
     * Must be between 1 and 365 days.
     * Concrete gains strength non-linearly with age.
     */
    @NotNull
    @Min(1)
    @Max(365)
    @Column(name = "age")
    private Integer age;

    /**
     * Predicted compressive strength in MPa.
     * Populated by the ML service after prediction.
     * Null until prediction is returned successfully.
     */
    @Column(name = "predicted_strength")
    private Double predictedStrength;

    /**
     * Identifier of the ML model version that produced the prediction.
     * Used for audit trail and model versioning.
     */
    @NotBlank
    @Column(name = "model_version", nullable = false)
    private String modelVersion;

    /**
     * Timestamp of when this prediction record was created.
     * Automatically set by Hibernate on insert — never updated.
     */
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}