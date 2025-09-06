-- Agregar campo fsm_order_id a account_analytic_line si no existe
-- Esto previene el error al instalar patco_core cuando hr_timesheet ya está instalado

DO $$
BEGIN
    -- Verificar si la columna ya existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'account_analytic_line' 
        AND column_name = 'fsm_order_id'
    ) THEN
        -- Agregar la columna fsm_order_id
        ALTER TABLE account_analytic_line 
        ADD COLUMN fsm_order_id INTEGER;
        
        -- Agregar índice para mejor rendimiento
        CREATE INDEX IF NOT EXISTS idx_account_analytic_line_fsm_order_id 
        ON account_analytic_line(fsm_order_id);
        
        RAISE NOTICE 'Campo fsm_order_id agregado a account_analytic_line';
    ELSE
        RAISE NOTICE 'Campo fsm_order_id ya existe en account_analytic_line';
    END IF;
END $$;