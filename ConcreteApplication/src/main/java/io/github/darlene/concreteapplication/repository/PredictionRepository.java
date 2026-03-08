package io.github.darlene.concreteapplication.repository;

import io.github.darlene.concreteapplication.entity.PredictionRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

/**
 * Repository interface for {@link PredictionRecord} database operations.
 *
 * <p>Extends {@link JpaRepository} to inherit standard CRUD operations
 * including save, findById, findAll and deleteById.
 * Spring Data JPA generates all SQL implementations automatically
 * at runtime — no implementation class is needed.</p>
 *
 * <p>Spring Boot detects this interface automatically through
 * component scanning — no {@code @Repository} annotation required.</p>
 *
 * @author Darlene
 * @version 1.0
 */
public interface PredictionRepository
        extends JpaRepository<PredictionRecord, Long> {

    /**
     * Retrieves all prediction records ordered by creation timestamp
     * in descending order — most recent predictions first.
     *
     * <p>Spring Data JPA derives the SQL query automatically
     * from this method name at runtime.</p>
     *
     * <p>Equivalent SQL:
     * {@code SELECT * FROM prediction_record ORDER BY created_at DESC}</p>
     *
     * @return list of all prediction records, most recent first
     */
    List<PredictionRecord> findAllByOrderByCreatedAtDesc();
}