-- Banking Model Validation System Database Schema

-- Models table
CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) UNIQUE NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    scorecard_type VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    description TEXT,
    version VARCHAR(50),
    owner VARCHAR(255),
    watsonx_asset_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Validations table
CREATE TABLE IF NOT EXISTS validations (
    id SERIAL PRIMARY KEY,
    validation_id VARCHAR(255) UNIQUE NOT NULL,
    model_id INTEGER REFERENCES models(id),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    results JSONB,
    document_path TEXT,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Validation metrics table
CREATE TABLE IF NOT EXISTS validation_metrics (
    id SERIAL PRIMARY KEY,
    validation_id VARCHAR(255) REFERENCES validations(validation_id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC,
    metric_category VARCHAR(50),
    dataset_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance tracking table
CREATE TABLE IF NOT EXISTS compliance_tracking (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES models(id),
    validation_id VARCHAR(255) REFERENCES validations(validation_id),
    compliance_framework VARCHAR(50) NOT NULL,
    component VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    findings TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id VARCHAR(255),
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_models_name ON models(model_name);
CREATE INDEX idx_validations_status ON validations(status);
CREATE INDEX idx_validations_model ON validations(model_id);
CREATE INDEX idx_compliance_model ON compliance_tracking(model_id);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);

-- Insert sample data
INSERT INTO models (model_name, product_type, scorecard_type, model_type, description, version, owner)
VALUES 
    ('Sample_Application_Scorecard', 'unsecured', 'application', 'XGBoost', 'Sample application scorecard for testing', '1.0', 'Model Risk Management'),
    ('Sample_Behavioral_Scorecard', 'revolving', 'behavioral', 'GLM', 'Sample behavioral scorecard for testing', '1.0', 'Credit Risk Team')
ON CONFLICT (model_name) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO validation_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO validation_user;

-- Made with Bob
