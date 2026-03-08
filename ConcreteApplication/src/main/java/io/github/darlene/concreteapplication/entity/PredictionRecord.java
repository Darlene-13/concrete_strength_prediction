package io.github.darlene.concreteapplication.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakrta.persistence.Table;
import jakarta.persistence.GeneratedValue;
import jakrta.persistence.Column;
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
 *  Represents a single prediction entity
 */


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
public class PredictionRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "cement")
    private Double cement;

    @Column(name = "water")
    private Double water;

    @Column(name = "blast_furnace_slag")
    private Double blastFurnaceSlag;

    @Column(name = "fly_ash")
    private Double flyAsh;

    @Column(name = "superplasticizer")
    private Double superplasticizer;

    @Column(name = "coarse_aggregate")
    private Double coarseAggregate;

    @Column(name = "fine_aggregate")
    private Double fineAggregate;

    @Column(name = "age")
    private Integer age;

    @Column(name = "predicted_strength")
    private Double predictedStrength;

    @Column(name = "model_version")
    private String modelVersion;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}