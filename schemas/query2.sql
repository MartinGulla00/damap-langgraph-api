CREATE TABLE `dw_cancelaciones` ( 
  `ID_Cancelacion_PK` int NOT NULL AUTO_INCREMENT,
  `ID_TipoCancelacion` int DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  `ID_Cuenta` int DEFAULT NULL,
  `ID_TipoMatching` int DEFAULT NULL,
  `NUM_PasoWorkflow` int DEFAULT NULL,
  `Umbral_Tolerancia` decimal(10,2) DEFAULT '0.00',
  `FLAG_CancelacionConAjuste` int DEFAULT '0',
  `Importe_Ajuste_Debe` decimal(15,2) DEFAULT '0.00',
  `Importe_Ajuste_Haber` decimal(15,2) DEFAULT '0.00',
  `Cod_AAAAMM_Ini` int DEFAULT NULL,
  `Cod_AAAAMM_Fin` int DEFAULT NULL,
  `Lista_AAAAMM` varchar(100) DEFAULT NULL,
  `FLAG_InterPeriodos` int DEFAULT '0',
  `Minima_Fecha_Contable` date DEFAULT NULL,
  `Maxima_Fecha_Contable` date DEFAULT NULL,
  `Minima_Fecha_Banco` date DEFAULT NULL,
  `Maxima_Fecha_Banco` date DEFAULT NULL,
  `TimeStamp_Creacion` datetime(3) DEFAULT NULL,
  `ID_User` int DEFAULT NULL,
  `DESC_Descripcion` varchar(1000) DEFAULT NULL,
  `ID_Registro_Lote_Proceso` bigint DEFAULT NULL,
  `id_grupo_conciliaciones` int DEFAULT NULL,
  `id_paso_datamatching` int DEFAULT NULL,
  `id_tipo_estado_conciliacion` int DEFAULT '1',
  `flag_caso_asociado` int DEFAULT '0',
  `id_caso_expediente` int DEFAULT NULL,
  `cant_partidas_conciliadas` int DEFAULT NULL,
  `flag_conciliacion_masiva` int DEFAULT '0',
) ENGINE=InnoDB AUTO_INCREMENT=6735192 DEFAULT CHARSET=utf8mb3;