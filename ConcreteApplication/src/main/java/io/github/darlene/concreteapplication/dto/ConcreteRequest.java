package io.github.darlene.concreteapplication.dto;


import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;


import lombok.Data;
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object representing an incoming concrete mix design request.
 *
 * <p>Carries and validates the raw mix ingredients submitted by the client
 * via the REST API. This object is never persisted directly to the database —
 * it is mapped to a {@link io.github.darlene.concreteapplication.entity.PredictionRecord}
 * by the service layer after prediction.</p>
 *
 * <p>Validation is applied at this layer to protect the application from
 * invalid or physically impossible mix designs before they reach
 * the ML service or database.</p>
 *
 * <p>All quantities are in kg/m³ except age which is in days.</p>
 *
 * @author Darlene
 * @version 1.0
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ConcreteRequest {

    /**
     * Cement content in kg/m³.
     * Primary binder in the mix — required in all concrete designs.
     * Must be a strictly positive value.
     */
    @NotNull(message = "Cement quantity cannot be null")
    @Positive(message = "Cement quantity must be greater than zero")
    private Double cement;

    /**
     * Water content in kg/m³.
     * Required for cement hydration.
     * Directly determines the water-to-cement ratio
     * which is the strongest predictor of compressive strength.
     */
    @NotNull(message = "Water volume cannot be null")
    @Positive(message = "Water volume must be greater than zero")
    private Double water;

    /**
     * Coarse aggregate content in kg/m³.
     * Forms the structural skeleton of the concrete mix.
     * Required in all concrete designs.
     */
    @NotNull(message = "Coarse aggregate quantity cannot be null")
    @Positive(message = "Coarse aggregate must be greater than zero")
    private Double coarseAggregate;

    /**
     * Fine aggregate (sand) content in kg/m³.
     * Fills voids between coarse aggregate particles
     * and improves workability and density of the mix.
     * Required in all concrete designs.
     */
    @NotNull(message = "Fine aggregate quantity cannot be null")
    @Positive(message = "Fine aggregate must be greater than zero")
    private Double fineAggregate;

    /**
     * Curing age of the concrete in days.
     * Concrete gains compressive strength non-linearly with age —
     * most strength gain occurs within the first 28 days.
     * Must be between 1 and 365 days inclusive.
     */
    @NotNull(message = "Age cannot be null")
    @Min(value = 1, message = "Age must be at least 1 day")
    @Max(value = 365, message = "Age cannot exceed 365 days")
    private Integer age;

    /**
     * Blast furnace slag content in kg/m³.
     * Optional supplementary cementitious material (SCM).
     * Slow-reacting — contributes more to long-term strength than early strength.
     * Zero indicates this mix does not use slag.
     */
    @NotNull(message = "Blast furnace slag quantity cannot be null")
    @PositiveOrZero(message = "Blast furnace slag cannot be negative")
    private Double blastFurnaceSlag;

    /**
     * Fly ash content in kg/m³.
     * Optional supplementary cementitious material (SCM).
     * Slowest-reacting SCM — primary contribution at 90+ days.
     * Zero indicates this mix does not use fly ash.
     */
    @NotNull(message = "Fly ash quantity cannot be null")
    @PositiveOrZero(message = "Fly ash cannot be negative")
    private Double flyAsh;

    /**
     * Superplasticizer content in kg/m³.
     * Optional chemical admixture that improves workability
     * and allows reduction of water content without loss of flowability,
     * indirectly improving compressive strength.
     * Zero indicates this mix does not use superplasticizer.
     */
    @NotNull(message = "Superplasticizer quantity cannot be null")
    @PositiveOrZero(message = "Superplasticizer cannot be negative")
    private Double superplasticizer;
}
