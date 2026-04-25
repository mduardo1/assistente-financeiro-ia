import re
import unicodedata
from datetime import date


class ParserService:
    EXPENSE_KEYWORDS = {"gastei", "paguei", "comprei", "saiu", "despesa", "gasto"}
    INCOME_KEYWORDS = {"recebi", "ganhei", "vendi", "entrou", "receita", "venda"}

    def parse_message(self, message: str) -> dict[str, str]:
        original_message = message.strip()

        if not original_message:
            raise ValueError("A mensagem do parser é obrigatória.")

        normalized_message = self._normalize(original_message)
        keyword = normalized_message.split()[0]
        transaction_type = self._resolve_type(keyword)

        amount_match = re.search(r"(?<!-)\b(\d+(?:[.,]\d{1,2})?)\b", normalized_message)
        if amount_match is None:
            raise ValueError("Não encontrei um valor financeiro na mensagem.")

        amount = amount_match.group(1).replace(",", ".")
        category = self._extract_category(normalized_message, keyword, amount_match.group(1))

        return {
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "description": original_message,
            "transaction_date": date.today().isoformat(),
        }

    def _resolve_type(self, keyword: str) -> str:
        if keyword in self.EXPENSE_KEYWORDS:
            return "expense"

        if keyword in self.INCOME_KEYWORDS:
            return "income"

        raise ValueError("Não consegui identificar se a mensagem é entrada ou saída.")

    def _extract_category(self, message: str, keyword: str, amount: str) -> str:
        message_without_prefix = re.sub(
            rf"^{re.escape(keyword)}\s+{re.escape(amount)}\s*",
            "",
            message,
        ).strip()

        patterns = [
            r"^(?:no|na|em|de|do|da)\s+(.+)$",
            r"^(?:para|pro|pra)\s+(.+)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, message_without_prefix)
            if match is not None:
                return match.group(1).strip()

        return message_without_prefix or "geral"

    def _normalize(self, value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.lower())
        return "".join(character for character in normalized if not unicodedata.combining(character))
